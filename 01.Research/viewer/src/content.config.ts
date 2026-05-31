import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// 01.Research/ 直下の Markdown を読み込むコンテンツコレクション。
// このビューアは 01.Research/viewer/ にあるため、親（= 01.Research）を base にする。
// リサーチは 01.Research 直下にフラット配置するため、再帰しない '*.md' で収集する。
// （'**/*.md' だと viewer 自身の node_modules / .astro キャッシュまで巻き込みループするため不可）
// frontmatter スキーマは .claude/skills/research-log/references/report-template.md と一致させること。
const research = defineCollection({
  loader: glob({ pattern: '*.md', base: '../' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default(''),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    category: z.string().optional().default('未分類'),
    sources: z
      .array(
        z.object({
          title: z.string(),
          url: z.string().url(),
          type: z.enum(['official', 'community']).optional(),
        })
      )
      .default([]),
    confidence: z.enum(['high', 'medium', 'low']).optional(),
  }),
});

export const collections = { research };
