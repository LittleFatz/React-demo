# Research Report Generation Workflow

This document provides detailed instructions for generating comprehensive research reports.

## Workflow Steps

### Step 1: Answer the Question with Claude AI

First, provide a comprehensive, well-structured answer to the user's question using Claude's knowledge base.

**Guidelines:**
- Provide detailed, technical explanations when appropriate
- Use clear sections and paragraphs
- Include examples where relevant
- Aim for 300-600 words depending on question complexity

**Example structure:**
```
Brief overview of the topic...

Key points:
1. First important aspect...
2. Second important aspect...
3. Third important aspect...

Detailed explanation of each point...

Practical considerations or examples...
```

### Step 2: Search Google for Top 10 Results

Use the `WebSearch` tool to find the top search results related to the question.

**Search strategy:**
- Use the exact question or a refined version as the search query
- Focus on keywords that will yield technical/authoritative sources
- Aim to retrieve at least 10 results

**Tool usage:**
```
WebSearch with query = user's question (or optimized version)
```

### Step 3: Extract Descriptions from Search Results

For each of the top 10 search results, extract:
- **Title**: The page title
- **URL**: The full URL
- **Description**: A brief description (use the snippet from search results, or use WebFetch to get page summary)

**Option A - Use search snippets:**
Most search results include a brief description/snippet. Use these directly if they're informative.

**Option B - Fetch page summaries (if needed):**
If search snippets are insufficient, use `WebFetch` tool to get better summaries:
```
WebFetch(url, prompt="Provide a 2-3 sentence summary of what this page covers")
```

**Important:** Balance thoroughness with efficiency. Only fetch pages if search snippets are unclear.

### Step 4: Generate Conclusion

Create a comprehensive conclusion that:
- Synthesizes Claude's answer with insights from search results
- Highlights common themes or consensus from multiple sources
- Notes any conflicting information or different approaches
- Provides actionable takeaways or recommendations
- Keeps it concise (150-300 words)

**Conclusion template:**
```
Based on both the AI analysis and top search results, [main finding]...

Key consensus points:
- Point 1 from multiple sources
- Point 2 from multiple sources

Additional insights from research:
- Unique perspective from source A
- Practical tip from source B

Recommendation/Final thoughts...
```

### Step 5: Generate the PDF Report

Create a JSON data file with all the collected information and pass it to the PDF generation script.

**Data structure:**
```json
{
  "question": "The original question",
  "claude_answer": "Claude's full answer from Step 1",
  "search_results": [
    {
      "title": "Article title",
      "url": "https://example.com/article",
      "description": "Brief description of the article content"
    }
    // ... up to 10 results
  ],
  "conclusion": "The synthesized conclusion from Step 4",
  "output_path": "path/to/output.pdf"
}
```

**Script execution:**
```bash
python3 scripts/generate_report.py data.json
```

The script will generate a modern, tech-style PDF with:
- Clean layout with blue accent colors
- Organized sections for Claude's answer, search results, and conclusion
- Clickable links to sources
- Professional formatting

## Tips for Quality Reports

1. **Answer quality:** Ensure Claude's answer is comprehensive but not overly verbose
2. **Search relevance:** Verify search results are actually relevant to the question
3. **Description clarity:** Make sure each source has a clear, informative description
4. **Conclusion synthesis:** Don't just repeat the answer; add value by integrating search findings
5. **Formatting:** Use proper paragraphs and line breaks in both answer and conclusion for readability

## Troubleshooting

**Issue: Search results not relevant**
- Refine the search query with more specific keywords
- Try alternative phrasings of the question

**Issue: PDF generation fails**
- Verify all required Python packages are installed (reportlab)
- Check that the JSON data structure is correct
- Ensure output path is writable

**Issue: Links not rendering in PDF**
- Verify URLs are complete and properly formatted
- Check that special characters in URLs are properly escaped
