#!/usr/bin/env node

import { Command } from 'commander';
import Parser from 'rss-parser';
import pc from 'picocolors';

const parser = new Parser();

// Simple relative time helper
function formatRelativeTime(dateString) {
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString || 'unknown date';
  
  const now = new Date();
  const diffMs = now - date;
  
  // Handle future dates or timezone skew
  if (diffMs < 0) return 'just now';
  
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDays = Math.floor(diffHr / 24);

  if (diffSec < 60) {
    return 'just now';
  } else if (diffMin < 60) {
    return `${diffMin}m ago`;
  } else if (diffHr < 24) {
    return `${diffHr}h ago`;
  } else if (diffDays < 7) {
    return `${diffDays}d ago`;
  } else {
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
}

// Split Google News title "Story Title - Source Name"
function parseTitleAndSource(title) {
  if (!title) return { title: 'No Title', source: 'Google News' };
  const parts = title.split(' - ');
  if (parts.length > 1) {
    const source = parts.pop().trim();
    const cleanTitle = parts.join(' - ').trim();
    return { title: cleanTitle, source };
  }
  return { title, source: 'Google News' };
}

const program = new Command();

program
  .name('google-news')
  .description('CLI tool to get the latest news from Google News')
  .version('1.0.0')
  .option('-s, --search <query>', 'Search for specific news topics')
  .option('-n, --limit <number>', 'Number of news items to display', '10')
  .option('-l, --lang <lang>', 'Language code (default: en)', 'en')
  .option('-r, --region <region>', 'Region code (default: US)', 'US')
  .action(async (options) => {
    const limit = parseInt(options.limit, 10);
    if (isNaN(limit) || limit <= 0) {
      console.error(pc.red('Error: Limit must be a positive number.'));
      process.exit(1);
    }

    const lang = options.lang.toLowerCase();
    const region = options.region.toUpperCase();
    const hl = lang.includes('-') ? lang : `${lang}-${region}`;
    const ceid = `${region}:${lang}`;

    let url = `https://news.google.com/rss?hl=${hl}&gl=${region}&ceid=${ceid}`;
    let modeText = 'Top Stories';

    if (options.search) {
      const encodedQuery = encodeURIComponent(options.search);
      url = `https://news.google.com/rss/search?q=${encodedQuery}&hl=${hl}&gl=${region}&ceid=${ceid}`;
      modeText = `Search results for: "${options.search}"`;
    }

    console.log();
    console.log(pc.cyan(pc.bold(' ┌──────────────────────────────────────────────┐')));
    console.log(pc.cyan(pc.bold(' │               GOOGLE NEWS CLI                │')));
    console.log(pc.cyan(pc.bold(' └──────────────────────────────────────────────┘')));
    console.log(` Mode:   ${pc.yellow(modeText)}`);
    console.log(` Region: ${pc.green(region)} | Language: ${pc.green(lang)}`);
    console.log(pc.dim(' ────────────────────────────────────────────────'));
    console.log(pc.blue(' Fetching latest updates...'));
    console.log();

    try {
      const feed = await parser.parseURL(url);
      
      if (!feed.items || feed.items.length === 0) {
        console.log(pc.yellow(' No news articles found.'));
        return;
      }

      const itemsToShow = feed.items.slice(0, limit);

      itemsToShow.forEach((item, index) => {
        const { title, source } = parseTitleAndSource(item.title);
        const timeAgo = formatRelativeTime(item.pubDate);
        
        // Print item index and title
        const numStr = pc.cyan(pc.bold(`${index + 1}.`));
        console.log(`${numStr} ${pc.bold(title)}`);
        
        // Print metadata line (Source, Time)
        const metaLine = `   ${pc.magenta(pc.bold(`[${source}]`))} • ${pc.dim(timeAgo)}`;
        console.log(metaLine);
        
        // Print URL
        console.log(`   ${pc.blue(pc.underline(item.link))}`);
        console.log();
      });

      console.log(pc.dim(` Showing ${itemsToShow.length} of ${feed.items.length} stories.`));
      console.log();
    } catch (error) {
      console.error(pc.red(`\n Error fetching news: ${error.message}`));
      console.error(pc.dim(' Please check your network connection or the language/region arguments.\n'));
      process.exit(1);
    }
  });

program.parse(process.argv);
