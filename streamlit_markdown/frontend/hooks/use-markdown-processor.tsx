import { CircleNotch, MathOperations, CheckFat, Copy, FlowArrow, Code } from "@phosphor-icons/react";
import { Root } from "hast";
import "highlight.js/styles/green-screen.css";
import mermaid from "mermaid";
import Link from "next/link";
import {
  Children,
  Fragment,
  createElement,
  isValidElement,
  useEffect,
  useMemo,
  useState,
  useRef,
} from "react";
import flattenChildren from "react-keyed-flatten-children";
import rehypeHighlight from "rehype-highlight";
import rehypeReact from "rehype-react";
import remarkGfm from "remark-gfm";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'
import { Plugin, unified } from "unified";
import { visit } from "unist-util-visit";
// @ts-expect-error
import { HtmlGenerator, parse } from "latex.js";
// import "node_modules/latex.js/dist/css/base.css"
// import "node_modules/latex.js/dist/css/katex.css"
import "katex/dist/katex.min.css"; // `rehype-katex` does not import the CSS for you;
// import "highlight.js/styles/base16/green-screen.css";
// import "@/styles/highlighting.green-screen.min.css";
export const ANCHOR_CLASS_NAME = "font-semibold underline text-emerald-700 underline-offset-[2px] decoration-1 hover:text-emerald-800 transition-colors";

// Mixing arbitrary Markdown + Capsize leads to lots of challenges
// with paragraphs and list items. This replaces paragraphs inside
// list items into divs to avoid nesting Capsize.
const rehypeListItemParagraphToDiv: Plugin<[], Root> = () => {
  return (tree) => {
    visit(tree, "element", (element) => {
      if (element.tagName === "li") {
        element.children = element.children.map((child) => {
          if (child.type === "element" && child.tagName === "p") {
            child.tagName = "div";
          }
          return child;
        });
      }
    });
    return tree;
  };
};

export const useMarkdownProcessor = (content: string) => {
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: "forest" });
  }, []);

  return useMemo(() => {
    return unified()
      .use(remarkParse)
      .use(remarkGfm)
      .use(remarkRehype)
      .use(remarkMath)
      .use(rehypeKatex)
      .use(rehypeHighlight, { ignoreMissing: true })
      .use(rehypeListItemParagraphToDiv)
      .use(rehypeReact, {
        createElement,
        Fragment,
        components: {
          a: ({ href, children }: JSX.IntrinsicElements["a"]) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className={ANCHOR_CLASS_NAME}
            >
              {children}
            </a>
          ),
          h1: ({ children, id }: JSX.IntrinsicElements["h1"]) => (
            <h1
              className="font-sans font-semibold text-2xl text-emerald-950 mb-6 mt-6"
              id={id}
            >
              {children}
            </h1>
          ),
          h2: ({ children, id }: JSX.IntrinsicElements["h2"]) => (
            <h2
              className="font-sans font-medium text-2xl text-emerald-950 mb-6 mt-6"
              id={id}
            >
              {children}
            </h2>
          ),
          h3: ({ children, id }: JSX.IntrinsicElements["h3"]) => (
            <h3
              className="font-sans font-semibold text-xl text-emerald-950 mb-6 mt-2"
              id={id}
            >
              {children}
            </h3>
          ),
          h4: ({ children, id }: JSX.IntrinsicElements["h4"]) => (
            <h4
              className="font-sans font-medium text-xl text-emerald-950 my-6"
              id={id}
            >
              {children}
            </h4>
          ),
          h5: ({ children, id }: JSX.IntrinsicElements["h5"]) => (
            <h5
              className="font-sans font-semibold text-lg text-emerald-950 my-6"
              id={id}
            >
              {children}
            </h5>
          ),
          h6: ({ children, id }: JSX.IntrinsicElements["h6"]) => (
            <h6
              className="font-sans font-medium text-lg text-emerald-950 my-6"
              id={id}
            >
              {children}
            </h6>
          ),
          p: (props: JSX.IntrinsicElements["p"]) => {
            return (
              <p className="font-sans text-sm text-emerald-900 mb-6">
                {props.children}
              </p>
            );
          },
          strong: ({ children }: JSX.IntrinsicElements["strong"]) => (
            <strong className="text-emerald-950 font-semibold">
              {children}
            </strong>
          ),
          em: ({ children }: JSX.IntrinsicElements["em"]) => (
            <em>{children}</em>
          ),
          code: CodeBlock,
          pre: ({ children }: JSX.IntrinsicElements["pre"]) => {
            return (
              <div className="relative mb-6">
                <pre className="p-4 rounded-lg border-2 border-emerald-200 bg-emerald-100 [&>code.hljs]:p-0 [&>code.hljs]:bg-transparent font-code text-sm overflow-x-auto flex items-start">
                  {children}
                </pre>
              </div>
            );
          },
          ul: ({ children }: JSX.IntrinsicElements["ul"]) => (
            <ul className="flex flex-col gap-3 text-emerald-900 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3">
              {Children.map(
                flattenChildren(children).filter(isValidElement),
                (child, index) => (
                  <li key={index} className="flex gap-2 items-start">
                    <div className="w-1 h-1 rounded-full bg-current block shrink-0 mt-1" />
                    {child}
                  </li>
                )
              )}
            </ul>
          ),
          ol: ({ children }: JSX.IntrinsicElements["ol"]) => (
            <ol className="flex flex-col gap-3 text-emerald-900 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3">
              {Children.map(
                flattenChildren(children).filter(isValidElement),
                (child, index) => (
                  <li key={index} className="flex gap-2 items-start">
                    <div
                      className="font-sans text-sm text-emerald-900 font-semibold shrink-0 min-w-[1.4ch]"
                      aria-hidden
                    >
                      {index + 1}.
                    </div>
                    {child}
                  </li>
                )
              )}
            </ol>
          ),
          li: ({ children }: JSX.IntrinsicElements["li"]) => (
            <div className="font-sans text-sm">{children}</div>
          ),
          table: ({ children }: JSX.IntrinsicElements["table"]) => (
            <div className="overflow-x-auto mb-6">
              <table className="table-auto border-2 border-emerald-200">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }: JSX.IntrinsicElements["thead"]) => (
            <thead className="bg-emerald-100">{children}</thead>
          ),
          th: ({ children }: JSX.IntrinsicElements["th"]) => (
            <th className="border-2 border-emerald-200 p-2 font-sans text-sm font-semibold text-emerald-950">
              {children}
            </th>
          ),
          td: ({ children }: JSX.IntrinsicElements["td"]) => (
            <td className="border-2 border-emerald-200 p-2 font-sans text-sm text-emerald-900">
              {children}
            </td>
          ),
          blockquote: ({ children }: JSX.IntrinsicElements["blockquote"]) => (
            <blockquote className="border-l-4 border-emerald-200 pl-2 text-emerald-900 italic">
              {children}
            </blockquote>
          ),
        },
      })
      .processSync(content).result;
  }, [content]);
};

const CodeBlock = ({ children, className }: JSX.IntrinsicElements["code"]) => {
  const [copied, setCopied] = useState(false);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    if (copied) {
      const interval = setTimeout(() => setCopied(false), 1000);
      return () => clearTimeout(interval);
    }
  }, [copied]);

  // Highlight.js adds a `className` so this is a hack to detect if the code block
  // is a language block wrapped in a `pre` tag.
  if (className) {
    const isMermaid = className.includes("language-mermaid");
    const isLatex = className.includes("language-latex");

    // show preview by default
    const [showMermaidPreview, setShowMermaidPreview] = useState(isMermaid);
    const [showLatexPreview, setShowLatexPreview] = useState(isLatex);

    return (
      <>
        {
          showLatexPreview ? (
            <div className={`flex-grow flex-shrink my-auto`}>
              <Latex content={children?.toString() ?? ""} />
            </div>
          ) : (
            showMermaidPreview ? (
              <div className={`flex-grow flex-shrink my-auto`}>
                <Mermaid content={children?.toString() ?? ""} />
              </div>
            ) : (
              <code ref={ref} className={`${className} flex-grow flex-shrink my-auto`}>
                {children}
              </code>
            )
          )
        }

        <div className="flex flex-col gap-1 flex-grow-0 flex-shrink-0">
          <button
            type="button"
            className="rounded-md p-1 text-emerald-900 hover:bg-emerald-200 border-2 border-emerald-200 transition-colors"
            aria-label="copy code to clipboard"
            title="Copy code to clipboard"
            onClick={() => {
              if (ref.current) {
                navigator.clipboard.writeText(ref.current.innerText ?? "");
                setCopied(true);
              }
            }}
          >
            {copied ? (
              <CheckFat className="w-4 h-4" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
          </button>
          {isMermaid ? (
            <>
              <button
                type="button"
                className="rounded-md p-1 text-emerald-900 hover:bg-emerald-200 border-2 border-emerald-200 transition-colors"
                aria-label={showMermaidPreview ? "Show Mermaid Code" : "Show Mermaid Diagram"}
                title={showMermaidPreview ? "Show Mermaid Code" : "Show Mermaid Diagram"}
                onClick={() => {
                  setShowMermaidPreview(!showMermaidPreview);
                }}
              >
                {showMermaidPreview ? (<Code className="w-4 h-4" />) : (<FlowArrow className="w-4 h-4" />)}
              </button>
            </>
          ) : null}
          {isLatex ? (
            <>
              <button
                type="button"
                className="rounded-md p-1 text-emerald-900 hover:bg-emerald-200 border-2 border-emerald-200 transition-colors"
                aria-label={showLatexPreview ? "Show Latex Code" : "Show Latex Diagram"}
                title={showLatexPreview ? "Show Latex Code" : "Show Latex Diagram"}
                onClick={() => {
                  setShowLatexPreview(!showLatexPreview);
                }}
              >
                {showLatexPreview ? (<Code className="w-4 h-4" />) : (<MathOperations className="w-4 h-4" />)}
              </button>
            </>
          ) : null}
        </div>
      </>
    );
  }

  return (
    <code className="inline-block font-code bg-emerald-100 text-emerald-950 p-0.5 -my-0.5 rounded">
      {children}
    </code>
  );
};

const Latex = ({ content }: { content: string }) => {
  const [diagram, setDiagram] = useState<string | boolean>(true);

  useEffect(() => {
    try {
      const generator = new HtmlGenerator({ hyphenate: false });
      const fragment = parse(content, { generator: generator }).domFragment();
      setDiagram(fragment.firstElementChild.outerHTML);
    } catch (error) {
      console.error(error);
      setDiagram(false);
    }
  }, [content]);

  if (diagram === true) {
    return (
      <div className="flex gap-2 items-center">
        <CircleNotch className="animate-spin w-4 h-4 text-emerald-900" />
        <p className="font-sans text-sm text-slate-700">Rendering diagram...</p>
      </div>
    );
  } else if (diagram === false) {
    return (
      <p className="font-sans text-sm text-slate-700">
        Unable to render this diagram.
      </p>
    );
  } else {
    return <div dangerouslySetInnerHTML={{ __html: diagram ?? "" }} />;
  }
};

const Mermaid = ({ content }: { content: string }) => {
  const [diagram, setDiagram] = useState<string | boolean>(true);

  useEffect(() => {
    const render = async () => {
      // Generate a random ID for mermaid to use.
      const id = `mermaid-svg-${Math.round(Math.random() * 10000000)}`;

      // Confirm the diagram is valid before rendering.
      if (await mermaid.parse(content, { suppressErrors: true })) {
        const { svg } = await mermaid.render(id, content);
        setDiagram(svg);
      } else {
        setDiagram(false);
      }
    };
    render();
  }, [content]);

  if (diagram === true) {
    return (
      <div className="flex gap-2 items-center">
        <CircleNotch className="animate-spin w-4 h-4 text-emerald-900" />
        <p className="font-sans text-sm text-slate-700">Rendering diagram...</p>
      </div>
    );
  } else if (diagram === false) {
    return (
      <p className="font-sans text-sm text-slate-700">
        Unable to render this diagram. Try copying it into the{" "}
        <Link
          href="https://mermaid.live/edit"
          className={ANCHOR_CLASS_NAME}
          target="_blank"
        >
          Mermaid Live Editor
        </Link>
        .
      </p>
    );
  } else {
    return <div dangerouslySetInnerHTML={{ __html: diagram ?? "" }} />;
  }
};
