import React from "react";
import { classNames } from "@/libs/class-names";
import { useMarkdownProcessor, ThemeColor, classNameByTheme } from "@/hooks/use-markdown-processor";

interface MarkdownContentProps {
  theme_color?: ThemeColor;
  content?: string;
  richContent?: boolean;
}

function MarkdownContent({
  theme_color = "green",
  content = "",
  richContent = true,
}: MarkdownContentProps): JSX.Element {
  const markdown_content = useMarkdownProcessor(content, theme_color);

  return (
    <div
      className={classNames(
        "rounded rounded-xl py-3 px-4 text-sm break-words overflow-x-auto shadow shadow relative border  ",
        "p-2 lg:p-6 border-2 rounded-lg min-w-0 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0",
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
