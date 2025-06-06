// Script to check all markdown files for broken links in non-interactive mode
const { execSync } = require('child_process');
const { readdirSync, statSync, writeFileSync } = require('fs');
const { join } = require('path');

// Recursively get all .md files in a directory
const getAllMdFiles = dir => 
  readdirSync(dir).reduce((files, file) => {
    const name = join(dir, file);
    if (statSync(name).isDirectory()) {
      return [...files, ...getAllMdFiles(name)];
    } else {
      return file.endsWith('.md') ? [...files, name] : files;
    }
  }, []);

// Check all markdown files
const mdFiles = getAllMdFiles('.');
let errorCount = 0;
const brokenLinks = [];

console.log(`Checking ${mdFiles.length} markdown files for broken links...`);

mdFiles.forEach(file => {
  try {
    // Run in quiet mode with JSON output
    const result = execSync(`npx markdown-link-check --quiet --json "${file}"`).toString();
    
    try {
      const linkCheckResult = JSON.parse(result);
      const fileErrors = linkCheckResult.filter(item => item.status === 'dead');
      
      if (fileErrors.length > 0) {
        console.log(`\n❌ ${file}: ${fileErrors.length} broken links`);
        errorCount += fileErrors.length;
        
        fileErrors.forEach(error => {
          const brokenLink = {
            file,
            link: error.link,
            statusCode: error.statusCode
          };
          brokenLinks.push(brokenLink);
          console.log(`   - ${error.link} (${error.statusCode})`);
        });
      } else {
        console.log(`✓ ${file}`);
      }
    } catch (parseError) {
      console.log(`⚠️ ${file}: Could not parse results`);
    }
  } catch (e) {
    console.error(`⚠️ Error checking ${file}`);
  }
});

// Generate report
if (brokenLinks.length > 0) {
  const report = {
    timestamp: new Date().toISOString(),
    totalFiles: mdFiles.length,
    totalBrokenLinks: errorCount,
    brokenLinks
  };
  
  writeFileSync('broken-links-report.json', JSON.stringify(report, null, 2));
  console.log(`\n❌ Link check complete. Found ${errorCount} broken links in ${brokenLinks.length} files.`);
  console.log(`Report saved to broken-links-report.json`);
} else {
  console.log(`\n✅ Link check complete. No broken links found in ${mdFiles.length} files.`);
}

process.exit(errorCount > 0 ? 1 : 0);
