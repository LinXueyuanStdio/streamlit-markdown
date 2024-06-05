import { classNames } from "@/libs/class-names";
import { CircleNotch, MathOperations, CheckFat, Copy, FlowArrow, Code } from "@phosphor-icons/react";
import { Root } from "hast";
import "highlight.js/styles/green-screen.css";
// import "https://unpkg.com/browse/@highlightjs/cdn-assets@11.6.0/styles/base16/green-screen.min.css";
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
export const ANCHOR_CLASS_NAME = "font-semibold underline underline-offset-[2px] decoration-1 transition-colors";

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
export type ThemeColor = "blue" | "orange" | "green";
export type ThemeScope = "bg" | "border" | "text" | "hover:bg" | "hover:text";

export function classNameByTheme(theme_color: ThemeColor, theme_scope: Array<ThemeScope> = ["bg", "border", "text"]) {
  const theme2scope = {
    "orange": {
      "bg": "bg-orange-100",
      "border": "border-orange-200",
      "text": "text-orange-900",
      "hover:bg": "hover:bg-orange-200",
      "hover:text": "hover:text-orange-800"
    },
    "green": {
      "bg": "bg-green-50",
      "border": "border-green-200",
      "text": "text-green-900",
      "hover:bg": "hover:bg-green-200",
      "hover:text": "hover:text-green-800"
    },
    "blue": {
      "bg": "bg-blue-50",
      "border": "border-blue-200",
      "text": "text-blue-900",
      "hover:bg": "hover:bg-blue-200",
      "hover:text": "hover:text-blue-800"
    }
  }
  return theme_scope.map((s) => {
    return theme2scope[theme_color][s];
  }).join(" ");
}

export const useMarkdownProcessor = (content: string, theme_color: ThemeColor = "green") => {
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
              className={classNames(
                ANCHOR_CLASS_NAME,
                classNameByTheme(theme_color, ["text", "hover:text"])
              )}
            >
              {children}
            </a>
          ),
          h1: ({ children, id }: JSX.IntrinsicElements["h1"]) => (
            <h1
              className={classNames(
                "font-sans font-semibold text-2xl mb-6 mt-6",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h1>
          ),
          h2: ({ children, id }: JSX.IntrinsicElements["h2"]) => (
            <h2
              className={classNames(
                "font-sans font-medium text-2xl mb-6 mt-6",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h2>
          ),
          h3: ({ children, id }: JSX.IntrinsicElements["h3"]) => (
            <h3
              className={classNames(
                "font-sans font-semibold text-xl mb-6 mt-2",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h3>
          ),
          h4: ({ children, id }: JSX.IntrinsicElements["h4"]) => (
            <h4
              className={classNames(
                "font-sans font-medium text-xl my-6",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h4>
          ),
          h5: ({ children, id }: JSX.IntrinsicElements["h5"]) => (
            <h5
              className={classNames(
                "font-sans font-semibold text-lg my-6",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h5>
          ),
          h6: ({ children, id }: JSX.IntrinsicElements["h6"]) => (
            <h6
              className={classNames(
                "font-sans font-medium text-lg my-6",
                classNameByTheme(theme_color, ["text"])
              )}
              id={id}
            >
              {children}
            </h6>
          ),
          p: (props: JSX.IntrinsicElements["p"]) => {
            return (
              <p className={classNames(
                "font-sans text-sm mb-6",
                classNameByTheme(theme_color, ["text"])
              )}>
                {props.children}
              </p>
            );
          },
          strong: ({ children }: JSX.IntrinsicElements["strong"]) => (
            <strong className={classNames(
              "font-semibold",
              classNameByTheme(theme_color, ["text"])
            )}>
              {children}
            </strong>
          ),
          em: ({ children }: JSX.IntrinsicElements["em"]) => (
            <em>{children}</em>
          ),
          code: ({ children, className }: JSX.IntrinsicElements["code"]) => CodeBlock({ children, className }, theme_color),
          pre: ({ children }: JSX.IntrinsicElements["pre"]) => {
            return (
              <div className="relative mb-6">
                <pre className={classNames(
                  "p-4 rounded-lg border-2 [&>code.hljs]:p-0 [&>code.hljs]:bg-transparent font-code text-sm overflow-x-auto flex items-start",
                  classNameByTheme(theme_color, ["border", "bg"])
                )}>
                  {children}
                </pre>
              </div>
            );
          },
          ul: ({ children }: JSX.IntrinsicElements["ul"]) => (
            <ul className={classNames(
              "flex flex-col gap-3 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3",
              classNameByTheme(theme_color, ["text"])
            )}>
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
            <ol className={classNames(
              "flex flex-col gap-3 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3",
              classNameByTheme(theme_color, ["text"])
            )}>
              {Children.map(
                flattenChildren(children).filter(isValidElement),
                (child, index) => (
                  <li key={index} className="flex gap-2 items-start">
                    <div
                      className={classNames(
                        "font-sans text-sm font-semibold shrink-0 min-w-[1.4ch]",
                        classNameByTheme(theme_color, ["text"])
                      )}
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
              <table className={classNames(
                "table-auto border-2",
                classNameByTheme(theme_color, ["border"])
              )}>
                {children}
              </table>
            </div>
          ),
          thead: ({ children }: JSX.IntrinsicElements["thead"]) => (
            <thead className={classNames(
              classNameByTheme(theme_color, ["bg"])
            )}>{children}</thead>
          ),
          th: ({ children }: JSX.IntrinsicElements["th"]) => (
            <th className={classNames(
              "border-2 p-2 font-sans text-sm font-semibold",
              classNameByTheme(theme_color, ["border", "text"])
            )}>
              {children}
            </th>
          ),
          td: ({ children }: JSX.IntrinsicElements["td"]) => (
            <td className={classNames(
              "border-2 p-2 font-sans text-sm",
              classNameByTheme(theme_color, ["border", "text"])
            )}>
              {children}
            </td>
          ),
          blockquote: ({ children }: JSX.IntrinsicElements["blockquote"]) => (
            <blockquote className={classNames(
              "border-l-4 pl-2 italic",
              classNameByTheme(theme_color, ["border", "text"])
            )}>
              {children}
            </blockquote>
          ),
        },
      })
      .processSync(content).result;
  }, [content, theme_color]);
};

const CodeBlock = ({ children, className }: JSX.IntrinsicElements["code"], theme_color: ThemeColor = "green") => {
  const isMermaid = className ? className.includes("language-mermaid") : false;
  const isLatex = className ? className.includes("language-latex"): false;

  // show preview by default
  const [showMermaidPreview, setShowMermaidPreview] = useState(isMermaid);
  const [showLatexPreview, setShowLatexPreview] = useState(isLatex);

  const [copied, setCopied] = useState(false);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    if (copied) {
      const interval = setTimeout(() => setCopied(false), 500);
      return () => clearTimeout(interval);
    }
  }, [copied]);

  // Highlight.js adds a `className` so this is a hack to detect if the code block
  // is a language block wrapped in a `pre` tag.
  if (className) {
    return (
      <>
        {
          showLatexPreview ? (
            <div className={`flex-grow flex-shrink my-auto`}>
              <Latex content={children?.toString() ?? ""} theme_color={theme_color} />
            </div>
          ) : (
            showMermaidPreview ? (
              <div className={`flex-grow flex-shrink my-auto`}>
                <Mermaid content={children?.toString() ?? ""} theme_color={theme_color} />
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
            className={classNames(
              "rounded-md p-1 border-2 transition-colors",
              classNameByTheme(theme_color, ["border", "text", "hover:bg"])
            )}
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
                className={classNames(
                  "rounded-md p-1 border-2 transition-colors",
                  classNameByTheme(theme_color, ["border", "text", "hover:bg"])
                )}
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
                className={classNames(
                  "rounded-md p-1 border-2 transition-colors",
                  classNameByTheme(theme_color, ["border", "text", "hover:bg"])
                )}
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
    <code className={classNames(
      "inline-block font-code p-0.5 -my-0.5 rounded",
      classNameByTheme(theme_color, ["text", "bg"])
    )}>
      {children}
    </code>
  );
};

const Latex = ({ content, theme_color = "green" }: { content: string, theme_color?: ThemeColor }) => {
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
        <CircleNotch className={classNames(
          "animate-spin w-4 h-4",
          classNameByTheme(theme_color, ["text"])
        )} />
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

const Mermaid = ({ content, theme_color = "green" }: { content: string, theme_color?: ThemeColor }) => {
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
        <CircleNotch className={classNames(
          "animate-spin w-4 h-4",
          classNameByTheme(theme_color, ["text"])
        )} />
        <p className="font-sans text-sm text-slate-700">Rendering diagram...</p>
      </div>
    );
  } else if (diagram === false) {
    return (
      <p className="font-sans text-sm text-slate-700">
        Unable to render this diagram. Try copying it into the{" "}
        <Link
          href="https://mermaid.live/edit"
          className={classNames(
            ANCHOR_CLASS_NAME,
            classNameByTheme(theme_color, ["text", "hover:text"])
          )}
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
