import React from "react";
import { classNames } from "@/libs/class-names";
import { useMarkdownProcessor } from "@/hooks/use-markdown-processor";

interface MarkdownContentProps {
  background_color?: "blue" | "orange" | "green";
  content?: string;
  partial?: boolean;
  nTokens?: number;
  richContent?: boolean;
}

function MarkdownContent({
  background_color = "green",
  content = "",
  richContent = true,
  partial = false,
  nTokens,
}: MarkdownContentProps): JSX.Element {
  const markdown_content = useMarkdownProcessor(content);

  return (
    <div
      className={classNames(
        "rounded rounded-xl py-3 px-4 text-sm break-words overflow-x-auto shadow shadow relative border  ",
        "p-2 lg:p-6 border-2 rounded-lg min-w-0 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0",
        background_color === "orange"
          ? "bg-orange-100 border-orange-200 text-orange-900"
          : background_color === "green"
            ? "bg-green-50 border-green-200 text-green-900"
            : "bg-blue-50 border-blue-200 text-blue-900",
        partial && "shadow shadow-md"
      )}
    >
      {nTokens ? (
        <div className="absolute bottom-1 right-1 p-1 text-xs opacity-50 bg-gray-200 rounded font-mono">
          {nTokens}
        </div>
      ) : null}
      <div>
        {!richContent ? (
          <div className="whitespace-pre-wrap prose prose-sm">{content}</div>
        ) : (
          // <div className="p-2 lg:p-6 border-2 border-emerald-200 rounded-lg bg-emerald-50 text-emerald-900 min-w-0 [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
          // </div>
          markdown_content
        )}
      </div>
    </div>
  );
}

export default MarkdownContent;
