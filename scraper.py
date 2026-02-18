#!/usr/bin/env python3
"""
Instagram Posts Batch Scraper
Extract engagement data from multiple Instagram posts using HikerAPI
"""

from hikerapi import Client
import pandas as pd
from datetime import datetime
import time
import random
from tqdm import tqdm
import sys
from pathlib import Path

# Import configuration
try:
    from config import (
        HIKERAPI_TOKEN, MAX_COMMENTS, MAX_LIKERS,
        DELAY_BETWEEN_REQUESTS, DELAY_BETWEEN_POSTS, DELAY_AFTER_ERROR,
        OUTPUT_DIRECTORY, OUTPUT_FILENAME,
        Colors, print_header, print_success, print_error, print_warning, print_info,
        validate_config
    )
except ImportError:
    print("[ERROR] config.py not found. Please ensure config.py is in the same directory.")
    sys.exit(1)

# ============================================
# UTILITIES
# ============================================

def random_sleep(min_sec, max_sec):
    """Sleep for random duration"""
    time.sleep(random.uniform(min_sec, max_sec))


def extract_shortcode(url):
    """Extract shortcode from Instagram URL"""
    return url.rstrip('/').split('/')[-1]


def load_urls_from_file(filepath):
    """Load URLs from text file (one URL per line)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and line.startswith('http')]
        return urls
    except FileNotFoundError:
        print_error(f"File not found: {filepath}")
        return []
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return []


def load_urls_from_python_file(filepath):
    """Load URLs from Python file (POST_URLS variable)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract POST_URLS list
        import re
        match = re.search(r'POST_URLS\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if match:
            urls_str = match.group(1)
            urls = re.findall(r'"([^"]+)"', urls_str)
            return urls
        else:
            print_error("POST_URLS not found in file")
            return []
    except Exception as e:
        print_error(f"Error reading Python file: {e}")
        return []


def ask_for_urls():
    """Interactive prompt to get URLs"""
    print_info("How would you like to provide URLs?")
    print("  1. Load from text file (.txt)")
    print("  2. Load from Python file (.py)")
    print("  3. Enter manually (comma-separated)")
    
    choice = input(f"{Colors.BLUE}Enter choice (1-3): {Colors.RESET}").strip()
    
    if choice == "1":
        filepath = input(f"{Colors.BLUE}Enter path to text file: {Colors.RESET}").strip().strip('"').strip("'")
        return load_urls_from_file(filepath)
    
    elif choice == "2":
        filepath = input(f"{Colors.BLUE}Enter path to Python file: {Colors.RESET}").strip().strip('"').strip("'")
        return load_urls_from_python_file(filepath)
    
    elif choice == "3":
        urls_input = input(f"{Colors.BLUE}Enter URLs (comma-separated): {Colors.RESET}").strip()
        urls = [url.strip() for url in urls_input.split(',') if url.strip()]
        return urls
    
    else:
        print_error("Invalid choice")
        return ask_for_urls()


# ============================================
# DATA EXTRACTION FUNCTIONS
# ============================================

def get_post_info(cl, url, pbar=None):
    """Retrieve post information"""
    shortcode = extract_shortcode(url)
    
    try:
        media = cl.media_by_code_v1(shortcode)
        
        post_info = {
            'original_url': url,
            'post_url': f"https://www.instagram.com/p/{shortcode}/",
            'shortcode': shortcode,
            'author': media.get('user', {}).get('username', ''),
            'author_full_name': media.get('user', {}).get('full_name', ''),
            'author_id': media.get('user', {}).get('pk', ''),
            'total_likes': media.get('like_count', 0),
            'total_comments': media.get('comment_count', 0),
            'publication_date': media.get('taken_at', ''),
            'media_type': media.get('media_type', ''),
            'caption': media.get('caption_text', '')[:500] if media.get('caption_text') else '',
            'location': media.get('location', {}).get('name', '') if media.get('location') else '',
            'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return post_info, media.get('pk', '')
        
    except Exception as e:
        if pbar:
            pbar.write(f"{Colors.RED}[ERROR]{Colors.RESET} Post info ({shortcode}): {e}")
        return None, None


def get_all_likers(cl, media_id, url, max_likers=None, pbar=None):
    """Retrieve users who liked the post"""
    shortcode = extract_shortcode(url)
    all_likers = []
    
    try:
        likers_list = cl.media_likers_gql(media_id=str(media_id))
        
        if isinstance(likers_list, list):
            for user in likers_list:
                if isinstance(user, dict):
                    all_likers.append({
                        'original_url': url,
                        'shortcode': shortcode,
                        'username': user.get('username', ''),
                        'full_name': user.get('full_name', ''),
                        'user_id': user.get('pk', ''),
                        'is_verified': user.get('is_verified', False),
                        'is_private': user.get('is_private', False),
                    })
                    
                    if max_likers and len(all_likers) >= max_likers:
                        break
        
        random_sleep(*DELAY_BETWEEN_REQUESTS)
        
    except Exception as e:
        if pbar:
            pbar.write(f"{Colors.YELLOW}[WARNING]{Colors.RESET} Likes ({shortcode}): {str(e)[:100]}")
    
    return all_likers


def parse_comment(comment_dict, url, is_reply=False, parent_username=''):
    """Parse a comment dictionary"""
    shortcode = extract_shortcode(url)
    created_at = comment_dict.get('created_at', 0)
    
    try:
        comment_date = datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else ''
    except:
        comment_date = str(created_at)
    
    user_data = comment_dict.get('user', {})
    
    return {
        'original_url': url,
        'shortcode': shortcode,
        'type': 'reply' if is_reply else 'comment',
        'parent_user': parent_username if is_reply else '',
        'username': user_data.get('username', ''),
        'full_name': user_data.get('full_name', '') or user_data.get('username', ''),
        'user_id': user_data.get('pk', '') or user_data.get('id', ''),
        'text': comment_dict.get('text', ''),
        'date': comment_date,
        'likes': comment_dict.get('comment_like_count', 0),
        'reply_count': comment_dict.get('child_comment_count', 0),
        'comment_id': comment_dict.get('pk', ''),
        'is_verified': user_data.get('is_verified', False)
    }


def get_comment_replies(cl, comment_id, media_id, comment_username, url, pbar=None):
    """Retrieve replies to a comment"""
    replies = []
    
    try:
        end_cursor = None
        
        while True:
            replies_data = cl.comments_threaded_chunk_gql(
                media_id=str(media_id),
                comment_id=str(comment_id),
                end_cursor=end_cursor
            )
            
            if not replies_data or not isinstance(replies_data, list):
                break
            
            replies_found = 0
            
            for page in replies_data:
                if isinstance(page, list):
                    for reply_dict in page:
                        if isinstance(reply_dict, dict):
                            replies.append(parse_comment(reply_dict, url, is_reply=True, parent_username=comment_username))
                            replies_found += 1
                elif isinstance(page, dict):
                    replies.append(parse_comment(page, url, is_reply=True, parent_username=comment_username))
                    replies_found += 1
            
            if replies_found == 0:
                break
            
            if len(replies_data) < 2:
                break
            
            last_page = replies_data[-1] if replies_data else []
            if last_page and isinstance(last_page, list) and len(last_page) > 0:
                last_reply = last_page[-1]
                if isinstance(last_reply, dict):
                    end_cursor = last_reply.get('pk', None)
            
            if not end_cursor:
                break
            
            random_sleep(0.5, 1.0)
        
    except Exception as e:
        pass  # Silent on reply errors
    
    return replies


def get_all_comments_with_replies(cl, media_id, url, max_comments=None, pbar=None):
    """Retrieve all comments and replies"""
    all_comments = []
    
    try:
        end_cursor = None
        
        while True:
            result = cl.comments_chunk_gql(
                media_id=str(media_id),
                end_cursor=end_cursor
            )
            
            if not result or not isinstance(result, list):
                break
            
            comments_found = 0
            
            for page_comments in result:
                if not isinstance(page_comments, list):
                    continue
                
                for comment_dict in page_comments:
                    if not isinstance(comment_dict, dict):
                        continue
                    
                    comment = parse_comment(comment_dict, url, is_reply=False)
                    all_comments.append(comment)
                    comments_found += 1
                    
                    # Get replies
                    child_count = comment_dict.get('child_comment_count', 0)
                    if child_count > 0:
                        replies = get_comment_replies(
                            cl, 
                            comment_dict.get('pk'),
                            media_id,
                            comment['username'],
                            url,
                            pbar
                        )
                        
                        if replies:
                            all_comments.extend(replies)
                        
                        random_sleep(0.8, 1.5)
                    
                    if max_comments and len(all_comments) >= max_comments:
                        break
                
                if max_comments and len(all_comments) >= max_comments:
                    break
            
            if comments_found == 0:
                break
            
            if max_comments and len(all_comments) >= max_comments:
                break
            
            if len(result) < 2:
                break
            
            random_sleep(*DELAY_BETWEEN_REQUESTS)
            
            last_page = result[-1] if result else []
            if last_page and isinstance(last_page, list) and len(last_page) > 0:
                last_comment = last_page[-1]
                if isinstance(last_comment, dict):
                    end_cursor = last_comment.get('pk', None)
            
            if not end_cursor:
                break
        
    except Exception as e:
        if pbar:
            pbar.write(f"{Colors.YELLOW}[WARNING]{Colors.RESET} Comments ({extract_shortcode(url)}): {str(e)[:100]}")
    
    return all_comments


# ============================================
# POST PROCESSING
# ============================================

def process_single_post(cl, url, pbar=None):
    """Process a single Instagram post"""
    shortcode = extract_shortcode(url)
    
    if pbar:
        pbar.set_description(f"{Colors.CYAN}Post {shortcode[:8]}... - Info{Colors.RESET}")
    
    # 1. Post info
    post_info, media_id = get_post_info(cl, url, pbar)
    if not post_info or not media_id:
        if pbar:
            pbar.write(f"{Colors.RED}[FAILED]{Colors.RESET} {shortcode}")
        return None, [], []
    
    random_sleep(*DELAY_BETWEEN_REQUESTS)
    
    # 2. Comments
    if pbar:
        pbar.set_description(f"{Colors.CYAN}Post {shortcode[:8]}... - Comments{Colors.RESET}")
    
    comments = get_all_comments_with_replies(cl, media_id, url, MAX_COMMENTS, pbar)
    
    random_sleep(*DELAY_BETWEEN_REQUESTS)
    
    # 3. Likes
    if pbar:
        pbar.set_description(f"{Colors.CYAN}Post {shortcode[:8]}... - Likes{Colors.RESET}")
    
    likers = get_all_likers(cl, media_id, url, MAX_LIKERS, pbar)
    
    # Statistics
    main_comments = [c for c in comments if c['type'] == 'comment']
    replies = [c for c in comments if c['type'] == 'reply']
    
    if pbar:
        pbar.write(f"{Colors.GREEN}[OK]{Colors.RESET} {shortcode[:10]}: {len(main_comments)}+{len(replies)} comments, {len(likers)} likes")
    
    return post_info, comments, likers


# ============================================
# SAVE RESULTS
# ============================================

def save_results(all_posts_info, all_comments, all_likers, output_dir, output_filename):
    """Save all data to a single CSV file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = output_path / f"{output_filename.replace('.csv', '')}_{timestamp}.csv"
    
    print_info("Saving data...")
    
    # Create unified data list
    all_data = []
    
    # 1. Add posts
    for post in all_posts_info:
        row = post.copy()
        row['data_type'] = 'POST'
        row['data_user'] = post['author']
        row['data_text'] = post['caption']
        row['data_date'] = post['publication_date']
        all_data.append(row)
    
    # 2. Add comments
    for comment in all_comments:
        row = {
            'original_url': comment['original_url'],
            'shortcode': comment['shortcode'],
            'data_type': comment['type'].upper(),  # 'COMMENT' or 'REPLY'
            'data_user': comment['username'],
            'data_full_name': comment['full_name'],
            'data_user_id': comment['user_id'],
            'data_text': comment['text'],
            'data_date': comment['date'],
            'data_likes': comment['likes'],
            'data_is_verified': comment['is_verified'],
            'parent_user': comment['parent_user'],
            'comment_id': comment['comment_id'],
            'reply_count': comment['reply_count']
        }
        all_data.append(row)
    
    # 3. Add likes
    for liker in all_likers:
        row = {
            'original_url': liker['original_url'],
            'shortcode': liker['shortcode'],
            'data_type': 'LIKE',
            'data_user': liker['username'],
            'data_full_name': liker['full_name'],
            'data_user_id': liker['user_id'],
            'data_is_verified': liker['is_verified'],
            'data_is_private': liker['is_private']
        }
        all_data.append(row)
    
    # Save CSV
    try:
        df_all = pd.DataFrame(all_data)
        
        # Reorder columns (original_url first)
        cols = df_all.columns.tolist()
        if 'original_url' in cols:
            cols.remove('original_url')
            cols = ['original_url'] + cols
            df_all = df_all[cols]
        
        df_all.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print_success(f"File saved: {filename}")
        print(f"  Total rows: {len(df_all):,}")
        print(f"  Posts: {len(all_posts_info)}")
        print(f"  Comments/Replies: {len(all_comments)}")
        print(f"  Likes: {len(all_likers)}")
        
        return filename
        
    except Exception as e:
        print_error(f"Save error: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main execution function"""
    print_header("INSTAGRAM BATCH SCRAPER")
    
    # Validate configuration
    if not validate_config():
        print_error("Please fix configuration errors in config.py")
        sys.exit(1)
    
    # Get URLs
    print_info("Loading URLs...")
    
    # Check if post_urls.txt or post_urls.py exists
    if Path("post_urls.txt").exists():
        urls = load_urls_from_file("post_urls.txt")
        print_success(f"Loaded {len(urls)} URLs from post_urls.txt")
    elif Path("post_urls.py").exists():
        urls = load_urls_from_python_file("post_urls.py")
        print_success(f"Loaded {len(urls)} URLs from post_urls.py")
    else:
        urls = ask_for_urls()
    
    if not urls:
        print_error("No URLs to process")
        sys.exit(1)
    
    # Display summary
    print()
    print_header("EXTRACTION SUMMARY")
    print(f"Posts to process: {Colors.BOLD}{len(urls)}{Colors.RESET}")
    print(f"Rate limiting: {DELAY_BETWEEN_REQUESTS[0]}-{DELAY_BETWEEN_REQUESTS[1]}s")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Initialize
    cl = Client(token=HIKERAPI_TOKEN)
    
    # Data collectors
    all_posts_info = []
    all_comments = []
    all_likers = []
    
    # Progress bar
    with tqdm(total=len(urls), desc=f"{Colors.CYAN}Progress{Colors.RESET}", unit="post") as pbar:
        for i, url in enumerate(urls):
            try:
                # Process post
                post_info, comments, likers = process_single_post(cl, url, pbar)
                
                if post_info:
                    all_posts_info.append(post_info)
                    all_comments.extend(comments)
                    all_likers.extend(likers)
                
                pbar.update(1)
                
                # Delay between posts (except last)
                if i < len(urls) - 1:
                    delay = random.uniform(*DELAY_BETWEEN_POSTS)
                    pbar.set_description(f"{Colors.YELLOW}Pause ({delay:.1f}s){Colors.RESET}")
                    time.sleep(delay)
                
            except KeyboardInterrupt:
                pbar.write(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.RESET} Manual stop (Ctrl+C)")
                break
            except Exception as e:
                pbar.write(f"{Colors.RED}[ERROR]{Colors.RESET} Critical error on {url}: {e}")
                time.sleep(DELAY_AFTER_ERROR)
                pbar.update(1)
    
    # Save results
    print()
    output_file = save_results(all_posts_info, all_comments, all_likers, OUTPUT_DIRECTORY, OUTPUT_FILENAME)
    
    # Final summary
    print()
    print_header("EXTRACTION COMPLETE")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print(f"{Colors.BOLD}Results:{Colors.RESET}")
    print(f"  Posts processed: {len(all_posts_info)}/{len(urls)}")
    print(f"  Total comments: {len(all_comments)}")
    print(f"  Total likes: {len(all_likers)}")
    if output_file:
        print(f"  Output file: {Colors.GREEN}{output_file}{Colors.RESET}")
    print(f"{'='*70}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[INTERRUPTED]{Colors.RESET} Manual stop")
    except Exception as e:
        print(f"\n{Colors.RED}[FATAL ERROR]{Colors.RESET} {e}")
        import traceback
        traceback.print_exc()