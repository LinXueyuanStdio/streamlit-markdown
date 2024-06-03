import { useRenderData } from "streamlit-component-lib-react-hooks";
import React from 'react';
import MarkdownContent from '@/components/markdown-content';

function StreamlitMarkdown() {
  const { theme, disabled, args } = useRenderData();

  return (
    <div>
      <MarkdownContent
        background_color={args.background_color}
        content={args.content}
        partial={args.partial}
        nTokens={args.nTokens}
        richContent={args.richContent}
      />
    </div>
  );
}

export default StreamlitMarkdown;
