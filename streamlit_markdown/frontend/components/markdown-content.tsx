import React from "react";
import { classNames } from "@/libs/class-names";
import { useMarkdownProcessor, ThemeColor, MermaidTheme, classNameByTheme } from "@/hooks/use-markdown-processor";

interface MarkdownContentProps {
  theme_color?: ThemeColor;
  content?: string;
  richContent?: boolean;
  mermaid_theme?: MermaidTheme;
  mermaid_theme_CSS?: string;
}

function MarkdownContent({
  theme_color = "green",
  content = "",
  richContent = true,
  mermaid_theme = "forest",
  mermaid_theme_CSS = "",
}: MarkdownContentProps): JSX.Element {
  const markdown_content = useMarkdownProcessor(content, theme_color, mermaid_theme, mermaid_theme_CSS);

  return (
    <div
      className={classNames(
        "rounded rounded-xl py-3 px-4 text-sm break-words overflow-x-auto shadow shadow relative ",
        "p-2 lg:p-6  rounded-lg min-w-0 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0",
        theme_color == "null" ? "" : "border-2 border",
        classNameByTheme(theme_color, ["bg", "border", "text"])
      )}
    >
      {richContent ? markdown_content : (
        <div className="whitespace-pre-wrap prose prose-sm">{content}</div>
      )}
    </div>
  );
}

export default MarkdownContent;
