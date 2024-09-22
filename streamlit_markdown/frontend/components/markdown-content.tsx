import React from "react";
import { classNames } from "@/libs/class-names";
import { useMarkdownProcessor, ThemeColor, MermaidTheme, CustomColor, CustomCSS, classNameByTheme } from "@/hooks/use-markdown-processor";

interface MarkdownContentProps {
  theme_color?: ThemeColor;
  content?: string;
  richContent?: boolean;
  mermaid_theme?: MermaidTheme;
  mermaid_theme_CSS?: string;
  custom_color: CustomColor;
  custom_css: CustomCSS;
}

function MarkdownContent({
  theme_color = "green",
  content = "",
  richContent = true,
  mermaid_theme = "forest",
  mermaid_theme_CSS = "",
  custom_color = {} as CustomColor,
  custom_css = {} as CustomCSS,
}: MarkdownContentProps): JSX.Element {
  console.log("content", content);
  console.log("theme_color", theme_color);
  console.log("mermaid_theme", mermaid_theme);
  console.log("mermaid_theme_CSS", mermaid_theme_CSS);
  console.log("custom_color", custom_color);
  console.log("custom_css", custom_css);
  const markdown_content = useMarkdownProcessor(content, theme_color, mermaid_theme, mermaid_theme_CSS, custom_color, custom_css);

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
