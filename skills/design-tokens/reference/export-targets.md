<!-- design:deferred -->
# Export Targets

Purpose: The output shape each consumer expects, and which one a project actually needs.
Read when: emitting tokens into a codebase.
Source: Tailwind, Style Dictionary, DTCG — the export formats of each, which move on their own release schedules.
Verified: 2026-08-21 — no automated check.

Emit the format the project actually consumes. Emitting all of them is noise.

## Decision

| Project | Emit |
|---------|------|
| Plain web / any framework | CSS custom properties |
| Tailwind v4 | CSS `@theme` block |
| Tailwind v3 | `tailwind.config` `theme.extend` |
| Multi-platform | DTCG JSON as source, Style Dictionary to build |
| iOS native | Swift enum / asset catalogue |
| Android native | Compose `Theme` object or `colors.xml` |
| Figma | DTCG JSON via a variables plugin |

## CSS custom properties

```css
:root {
  /* primitives */
  --gray-0: #ffffff;
  --gray-50: #f7f8fa;
  --gray-950: #0d0f13;
  --accent-400: #7aa2ff;
  --accent-600: #3560d8;

  /* semantics */
  --color-bg-canvas: var(--gray-0);
  --color-text-primary: var(--gray-950);   /* 19.18:1 on canvas */
  --color-action-bg: var(--accent-600);

  /* scales */
  --space-4: 1rem;
  --radius-md: 0.5rem;
  --text-base: 1rem;
}
```

Rules: `rem` for anything that should respond to the user's font size (type, spacing around type); `px` for hairlines, radii, and shadow offsets.

## Tailwind v4

```css
@import "tailwindcss";

@theme {
  --color-canvas: var(--gray-0);
  --color-surface: var(--gray-0);
  --color-text-primary: var(--gray-950);
  --spacing-4: 1rem;
  --radius-md: 0.5rem;
}
```

Tailwind derives utility names from the token names, so the grammar here *is* the class API. Decide it deliberately: `--color-text-primary` yields `text-text-primary`, which stutters — prefer `--color-primary` under Tailwind's own namespace rules. This is the rule-8 exception to `naming.md`'s anti-pattern list: the framework's grammar wins when the project adopts it.

## Style Dictionary

```js
// config.js
export default {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "dist/css/",
      files: [{ destination: "tokens.css", format: "css/variables" }],
    },
    ios: {
      transformGroup: "ios-swift",
      buildPath: "dist/swift/",
      files: [{ destination: "Tokens.swift", format: "ios-swift/enum.swift" }],
    },
    android: {
      transformGroup: "compose",
      buildPath: "dist/compose/",
      files: [{ destination: "Tokens.kt", format: "compose/object" }],
    },
  },
};
```

DTCG JSON is the source of truth; every platform file is generated. A hand-edited generated file is a bug.

## Swift

```swift
enum Color {
    static let textPrimary = SwiftUI.Color("TextPrimary")   // asset catalogue, light+dark
    static let actionBg    = SwiftUI.Color("ActionBg")
}
enum Space {
    static let s4: CGFloat = 16
}
```

Prefer an asset catalogue for colour so the system handles light/dark and high contrast; use a Swift enum for dimensions.

## Compose

```kotlin
object Space { val s4 = 16.dp }

@Immutable
data class AppColors(
    val textPrimary: Color,
    val actionBg: Color,
)

val LightColors = AppColors(textPrimary = Color(0xFF0D0F13), actionBg = Color(0xFF3560D8))
val DarkColors  = AppColors(textPrimary = Color(0xFFE8EAF0), actionBg = Color(0xFF7AA2FF))
```

## What ships alongside the export

1. A change log naming added, changed, and deprecated tokens.
2. The find/replace mapping for any rename.
3. The contrast table, so reviewers can re-verify without re-measuring.
4. A statement of which file is the source of truth and which are generated.
