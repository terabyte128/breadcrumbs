#!/usr/local/bin/python3
# -*- coding: ascii -*-

import sys
import subprocess
import time
import argparse

def main():
	parser = argparse.ArgumentParser(description="Create new Jekyll pages and publish to GitHub")
	subparsers = parser.add_subparsers(dest="action")
	subparsers.required = True

	new_page_cmd = subparsers.add_parser("newpage", aliases=["np"])
	new_page_cmd.add_argument("title")
	new_page_cmd.add_argument("--layout", "-l", default="page")
	new_page_cmd.add_argument("--filetype", "-f", choices=["md", "html"], default="md")
	new_page_cmd.add_argument("--permalink", "-p", action="store_true")
	new_page_cmd.add_argument("--directory", "-d")
	new_page_cmd.set_defaults(func=new_page)

	new_blog_cmd = subparsers.add_parser("newblog", aliases=["nb"])
	new_blog_cmd.add_argument("title")
	new_blog_cmd.add_argument("--layout", "-l", default="post")
	new_blog_cmd.add_argument("--filetype", "-f", choices=["md", "html"], default="md")
	new_blog_cmd.set_defaults(func=new_blog_post)

	git_cmd = subparsers.add_parser("git")
	git_cmd.add_argument("--commit", "-c")
	git_cmd.add_argument("--publish", "-p", action="store_true")
	git_cmd.set_defaults(func=git)

	args = parser.parse_args()
	args.func(args)

def write_file(name, **kwargs):
	f = open("%s" % name, 'w')
	f.write("---\n")
	for k, v in kwargs.items():
		f.write("%s: %s\n" % (k, v))
	f.write("---\n")
	f.close()	

def new_page(args):
	filename = args.title.replace(" ", "_").lower()
	
	file_args = {
		'layout': args.layout,
		'title': args.title
	}

	if args.directory:
		file_path = "%s/%s.%s" % (args.directory, filename, args.filetype)
	else:
		file_path = "%s.%s" % (filename, args.filetype)

	if args.permalink:
		file_args['permalink'] = "/%s" % filename

	write_file(file_path, **file_args)

def new_blog_post(args):
	datestr = time.strftime("%Y-%m-%d")
	filename = "_posts/" + datestr + "-" + args.title.replace(" ", "-").lower()
	
	file_args = {
		'layout': args.layout,
		'title': args.title,
		'categories': '',
		'date': time.strftime("%Y-%m-%d %H:%M:%S %z")
	}
	
	write_file("%s.%s" % (filename, args.filetype), **file_args)
	
def git(args):
	if args.commit is not None and args.commit == "":
		print("Error: commit message cannot be empty.", file=sys.stderr)
		sys.exit(1)

	if args.commit is not None:
		subprocess.call(['git', 'add', '-A'])
		subprocess.call(['git', 'commit', '-m', args.commit])

	if args.publish:
		subprocess.call(['git', 'push'])

if __name__ == "__main__":
	main()