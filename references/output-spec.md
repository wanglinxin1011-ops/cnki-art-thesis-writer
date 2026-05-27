# Output Specification

## Word Document Structure

Use this structure for the final `.docx` unless the user supplies a school template:

1. Chapter title
2. Chapter draft body
3. Viewpoint-source matrix
4. GB/T 7714 references
5. Issues requiring user confirmation
6. Unavailable literature
7. Retrieval and screening notes

## Chapter Body

- Write in Chinese unless the user requests another language.
- Use formal, restrained, logically clear academic prose.
- Avoid casual wording, marketing language, hollow praise, unsupported grand claims, and exclamation marks.
- Use heading levels suitable for a thesis chapter. Create modest second/third-level headings only when needed.

### Preset Writing Style (Chinese Art History)

Use the following as the default prose style. The user may supply a writing sample to override it.

**Narrative flow**: Evidence-first. Open paragraphs with archaeological or historical facts (unearthed artifacts, dates, regions, quantities), then draw interpretive conclusions. Use transitional phrases like `由此可见`, `可见`, `此处提到的`, `这也印证了`, `值得注意的是` to connect evidence to analysis.

**Concrete specificity**: Always name specific artifacts, sites, periods, and social groups. Prefer `战国时期楚国的漆器制造行业繁荣发展，造型美、样式新、器种多、产量大` over vague statements like `这一时期漆器发展很快`.

**Citation format**: Use bracketed reference-number-plus-page format `[n]page`, placed immediately after the cited sentence or clause—not inline `（来源：Author，Title，第X页）`. Examples:
  - `……制作精美的饮食器具——漆杯的景象：[3]228`
  - `贾贱而用不殊。[3]228`
  - `故一杯棬用百人之力，一屏风就万人之功，其为害亦多矣。[3]247`
  - Multiple sources: `……具有重要的历史意义。[2]45-48; [4]15-20`

**Primary source quotation**: When citing ancient texts, quote the original passage in a separate indented paragraph, followed by the `[n]page` citation. Then provide modern-language interpretation beginning with `此处提到的` or similar.

**Paragraph structure**: Moderate length (4-8 sentences). No bullet-point list style in body text. Let paragraphs build a cumulative argument.

**Register**: Formal, restrained Chinese academic register—no colloquialisms, no hollow praise. Let facts and analysis carry the argument.

## Viewpoint-Source Matrix

Include a table with these columns:

| 观点 | 来源文献 | 页码 | 文献章节/位置 | 原文摘录 | 使用方式 | 可靠性/备注 |
|---|---|---|---|---|---|---|

Usage types:
- 直接引用
- 转述
- 综合归纳
- 灵感启发

Excerpt rules:
- Use only short excerpts needed for verification.
- Avoid long continuous copied text.
- If exact page or excerpt cannot be extracted, write `需用户核查` and explain why.

## User Confirmation Section

List items that need the user's judgment, such as:
- Interpretations of artworks, artists, exhibitions, or styles not directly established by the literature
- Claims based on the user's own research object or practice
- Supervisor/school preference questions
- Claims where literature evidence is indirect or divided

Labels:
- `待用户确认`
- `证据不足`
- `存在争议`
- `页码需核查`

## Unavailable Literature

For each unavailable paper, record:
- Title, author
- CNKI link or identifying information
- Reason unavailable
- Whether the user should manually upload it
- Whether it was excluded or only used as metadata

## GB/T 7714 References

Generate from reliable metadata. Include as available:
- Author, title, literature type, journal/school/publisher, year, volume/issue, page range, DOI or CNKI URL

If metadata is incomplete, keep the entry but mark missing fields as `待补全`.

## Final Response To User

When delivering the document, briefly state:
- The output file path
- How many papers were found, deep-read, light-read, and unavailable
- Any uncertain page numbers or extraction limitations
- That the user should verify sources before submission
