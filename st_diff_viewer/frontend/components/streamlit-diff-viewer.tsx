import { useRenderData } from "streamlit-component-lib-react-hooks";
import React from 'react';
import ReactDiffViewer from 'react-diff-viewer';

function StreamlitDiffViewer() {
  const { theme, disabled, args } = useRenderData();

  return (
    <div>
      <ReactDiffViewer
        oldValue={args.oldText}
        newValue={args.newText}
        splitView={args.splitView}
        disableWordDiff={args.disabledWordDiff}
        leftTitle={args.leftTitle}
        rightTitle={args.rightTitle}
        useDarkTheme={args.useDarkTheme}
        extraLinesSurroundingDiff={args.extraLinesSurroundingDiff}
        hideLineNumbers={args.hideLineNumbers}
        highlightLines={args.highlightLines}
      />
    </div>
  );
}

export default StreamlitDiffViewer;
