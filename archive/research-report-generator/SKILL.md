---
name: research-report-generator
description: >
  Generate comprehensive research reports combining Claude AI analysis with Google search results.
  Use when the user requests: (1) Research reports on technical questions with web research,
  (2) Analysis combining AI insights and current web sources, (3) PDF reports synthesizing
  multiple information sources, (4) Commands like /summarise-claude-google. Produces modern,
  tech-style PDF reports with Claude's answer, top 10 search results, and synthesized conclusions.
---

# Research Report Generator

Generate comprehensive PDF research reports that combine Claude AI's deep analysis with current web search results.

## Overview

This skill creates professional research reports by:
1. Providing Claude's in-depth answer to a question
2. Searching Google for the top 10 most relevant sources
3. Synthesizing findings into a cohesive conclusion
4. Generating a modern, tech-style PDF report

The output is a clean, professional PDF with light background and blue tech accents, organized into clear sections.

## Workflow

### Step 1: Provide Claude's Analysis

Answer the user's question comprehensively using Claude's knowledge base.

**Guidelines:**
- Provide detailed, technical explanations for complex topics
- Structure the answer with clear paragraphs
- Include examples or code snippets where relevant
- Aim for 300-600 words depending on complexity

**Example for "How does Spring resolve circular dependencies?":**
```
Spring Framework handles circular dependencies through a three-level cache system...

The resolution process works as follows:
1. Early reference creation...
2. Proxy injection for AOP...
3. Final initialization...

Code example:
[relevant code snippet]

Best practices and considerations...
```

### Step 2: Search for Top Sources

Use the `WebSearch` tool to find the most relevant sources.

**Search strategy:**
- Use the user's question or an optimized version as the search query
- Focus on technical keywords for better results
- Retrieve at least 10 results

Example:
```
WebSearch(query="spring circular dependency resolution")
```

### Step 3: Extract Source Information

For each of the top 10 search results, collect:
- **Title**: The page/article title
- **URL**: Complete URL
- **Description**: 2-3 sentence summary

**Two approaches:**

**Option A - Use search snippets (preferred for efficiency):**
Search results typically include brief descriptions. Use these if they're clear and informative.

**Option B - Fetch page summaries (if needed):**
If snippets are unclear, use `WebFetch`:
```
WebFetch(url, prompt="Summarize this page in 2-3 sentences")
```

Balance thoroughness with efficiency—only fetch pages when necessary.

### Step 4: Create Synthesized Conclusion

Write a conclusion (150-300 words) that:
- Combines Claude's answer with insights from search results
- Highlights consensus or common themes across sources
- Notes different approaches or conflicting information
- Provides actionable recommendations or key takeaways

**Template:**
```
Based on the AI analysis and top search results, [main finding]...

Key consensus points:
- Common theme 1 across multiple sources
- Common theme 2 validated by research

Additional insights:
- Unique perspective from authoritative source
- Practical application or tip

Final recommendation...
```

### Step 5: Generate the PDF Report

Create a temporary JSON file with all collected data, then run the PDF generation script.

**Data structure:**
```json
{
  "question": "User's original question",
  "claude_answer": "Full answer from Step 1",
  "search_results": [
    {
      "title": "Article Title",
      "url": "https://example.com/article",
      "description": "Brief 2-3 sentence description"
    }
    // ... up to 10 results
  ],
  "conclusion": "Synthesized conclusion from Step 4",
  "output_path": "path/to/research_report.pdf"
}
```

**Execute the script:**
```bash
python3 scripts/generate_report.py data.json
```

The script generates a modern PDF with:
- Light background with blue tech accents
- Organized sections: Claude's analysis, search results, conclusion
- Clickable source links
- Professional typography and spacing
- Numbered search results with clear formatting

**After generation:**
- Delete the temporary JSON file
- Present the PDF path to the user
- Optionally display a brief summary of what was included

## Quality Guidelines

**Claude's Answer:**
- Comprehensive but focused
- Well-structured with clear sections
- Technical accuracy is paramount
- Include practical examples

**Search Results:**
- Verify relevance before including
- Ensure descriptions are informative
- Prioritize authoritative sources
- Check that URLs are valid

**Conclusion:**
- Add value beyond just repeating the answer
- Synthesize patterns from multiple sources
- Be specific about recommendations
- Keep it actionable

## Detailed Workflow Reference

For comprehensive workflow details, troubleshooting, and advanced tips, see [references/workflow.md](references/workflow.md).

## Resources

### scripts/generate_report.py

Python script that generates the PDF report. Requires the `reportlab` library.

**Installation:**
```bash
pip3 install reportlab
```

**Usage:**
```bash
python3 scripts/generate_report.py <data.json>
```

Creates a professional PDF with modern design, blue color scheme, and organized sections.

### references/workflow.md

Detailed workflow documentation including:
- Step-by-step instructions for each phase
- Search optimization strategies
- Conclusion synthesis templates
- Troubleshooting common issues
- Quality assurance tips
