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
import { Streamlit } from "streamlit-component-lib"
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
export type ThemeColor = "blue" | "orange" | "green" | "red" | "purple" | "pink" | "indigo" | "yellow" | "teal" | "cyan" | "gray" | "slate" | "dark" | "light" | "null" | "custom";
export type ThemeScope = "bg" | "border" | "text" | "hover_bg" | "hover_text";
export type MermaidTheme = string | 'default' | 'forest' | 'dark' | 'neutral' | 'null';
export type CustomColor = {
  bg: string;
  border: string;
  text: string;
  hover_bg: string;
  hover_text: string;
}

export type CustomCSS = {
  a_class: string,
  h1_class: string,
  h2_class: string,
  h3_class: string,
  h4_class: string,
  h5_class: string,
  h6_class: string,
  p_class: string,
  strong_class: string,
  em_class: string,
  code_class: string,
  code_button_class: string,
  code_latex_class: string,
  code_mermaid_class: string,
  pre_class: string,
  ul_class: string,
  ol_class: string,
  li_class: string,
  table_class: string,
  thead_class: string,
  th_class: string,
  td_class: string,
  blockquote_class: string,
}

export function classNameByTheme(theme_color: ThemeColor, theme_scope: Array<ThemeScope> = ["bg", "border", "text"], custom_colors: CustomColor = {
  "bg": "",
  "border": "",
  "text": "",
  "hover_bg": "hover:bg-gray-100",
  "hover_text": "hover:text-gray-900"
}) {
  const theme2scope = {
    "custom": custom_colors,
    "orange": {
      "bg": "bg-orange-100",
      "border": "border-orange-200",
      "text": "text-orange-900",
      "hover_bg": "hover:bg-orange-200",
      "hover_text": "hover:text-orange-800"
    },
    "green": {
      "bg": "bg-green-50",
      "border": "border-green-200",
      "text": "text-green-900",
      "hover_bg": "hover:bg-green-200",
      "hover_text": "hover:text-green-800"
    },
    "blue": {
      "bg": "bg-blue-50",
      "border": "border-blue-200",
      "text": "text-blue-900",
      "hover_bg": "hover:bg-blue-200",
      "hover_text": "hover:text-blue-800"
    },
    "red": {
      "bg": "bg-red-50",
      "border": "border-red-200",
      "text": "text-red-900",
      "hover_bg": "hover:bg-red-200",
      "hover_text": "hover:text-red-800"
    },
    "purple": {
      "bg": "bg-purple-50",
      "border": "border-purple-200",
      "text": "text-purple-900",
      "hover_bg": "hover:bg-purple-200",
      "hover_text": "hover:text-purple-800"
    },
    "pink": {
      "bg": "bg-pink-50",
      "border": "border-pink-200",
      "text": "text-pink-900",
      "hover_bg": "hover:bg-pink-200",
      "hover_text": "hover:text-pink-800"
    },
    "indigo": {
      "bg": "bg-indigo-50",
      "border": "border-indigo-200",
      "text": "text-indigo-900",
      "hover_bg": "hover:bg-indigo-200",
      "hover_text": "hover:text-indigo-800"
    },
    "yellow": {
      "bg": "bg-yellow-50",
      "border": "border-yellow-200",
      "text": "text-yellow-900",
      "hover_bg": "hover:bg-yellow-200",
      "hover_text": "hover:text-yellow-800"
    },
    "teal": {
      "bg": "bg-teal-50",
      "border": "border-teal-200",
      "text": "text-teal-900",
      "hover_bg": "hover:bg-teal-200",
      "hover_text": "hover:text-teal-800"
    },
    "cyan": {
      "bg": "bg-cyan-50",
      "border": "border-cyan-200",
      "text": "text-cyan-900",
      "hover_bg": "hover:bg-cyan-200",
      "hover_text": "hover:text-cyan-800"
    },
    "gray": {
      "bg": "bg-gray-50",
      "border": "border-gray-200",
      "text": "text-gray-900",
      "hover_bg": "hover:bg-gray-200",
      "hover_text": "hover:text-gray-800"
    },
    "slate": {
      "bg": "bg-slate-50",
      "border": "border-slate-200",
      "text": "text-slate-900",
      "hover_bg": "hover:bg-slate-200",
      "hover_text": "hover:text-slate-800"
    },
    "dark": {
      "bg": "bg-gray-900",
      "border": "border-gray-800",
      "text": "text-gray-100",
      "hover_bg": "hover:bg-gray-800",
      "hover_text": "hover:text-gray-100"
    },
    "light": {
      "bg": "bg-white",
      "border": "border-gray-200",
      "text": "text-gray-900",
      "hover_bg": "hover:bg-gray-100",
      "hover_text": "hover:text-gray-900"
    },
    "null": {
      "bg": "",
      "border": "",
      "text": "",
      "hover_bg": "hover:bg-gray-100",
      "hover_text": "hover:text-gray-900"
    }
  }
  return theme_scope.map((s) => {
    return theme2scope[theme_color][s];
  }).join(" ");
}

export const useMarkdownProcessor = (
  content: string,
  theme_color: ThemeColor = "green",
  mermaid_theme: MermaidTheme = "default",
  mermaid_theme_CSS: string | undefined = undefined,
  custom_color: CustomColor = {} as CustomColor,
  custom_css: CustomCSS = {} as CustomCSS,
) => {
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: mermaid_theme, themeCSS: mermaid_theme_CSS });
  }, [mermaid_theme, mermaid_theme_CSS]);

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
              className={custom_css.a_class.length > 0 ? custom_css.a_class : classNames(
                ANCHOR_CLASS_NAME,
                classNameByTheme(theme_color, ["text", "hover_text"], custom_color),
              )}
            >
              {children}
            </a>
          ),
          h1: ({ children, id }: JSX.IntrinsicElements["h1"]) => (
            <h1
              className={custom_css.h1_class.length > 0 ? custom_css.h1_class : classNames(
                "font-sans font-semibold text-2xl mb-6 mt-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h1>
          ),
          h2: ({ children, id }: JSX.IntrinsicElements["h2"]) => (
            <h2
              className={custom_css.h2_class.length > 0 ? custom_css.h2_class : classNames(
                "font-sans font-medium text-2xl mb-6 mt-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h2>
          ),
          h3: ({ children, id }: JSX.IntrinsicElements["h3"]) => (
            <h3
              className={custom_css.h3_class.length > 0 ? custom_css.h3_class : classNames(
                "font-sans font-semibold text-xl mb-6 mt-2",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h3>
          ),
          h4: ({ children, id }: JSX.IntrinsicElements["h4"]) => (
            <h4
              className={custom_css.h4_class.length > 0 ? custom_css.td_class : classNames(
                "font-sans font-medium text-xl my-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h4>
          ),
          h5: ({ children, id }: JSX.IntrinsicElements["h5"]) => (
            <h5
              className={custom_css.h5_class.length > 0 ? custom_css.h5_class : classNames(
                "font-sans font-semibold text-lg my-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h5>
          ),
          h6: ({ children, id }: JSX.IntrinsicElements["h6"]) => (
            <h6
              className={custom_css.h6_class.length > 0 ? custom_css.h6_class : classNames(
                "font-sans font-medium text-lg my-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}
              id={id}
            >
              {children}
            </h6>
          ),
          p: (props: JSX.IntrinsicElements["p"]) => {
            return (
              <p className={custom_css.p_class.length > 0 ? custom_css.p_class : classNames(
                "font-sans text-sm mb-6",
                classNameByTheme(theme_color, ["text"], custom_color),
              )}>
                {props.children}
              </p>
            );
          },
          strong: ({ children }: JSX.IntrinsicElements["strong"]) => (
            <strong className={custom_css.strong_class.length > 0 ? custom_css.strong_class : classNames(
              "font-semibold",
              classNameByTheme(theme_color, ["text"], custom_color),
            )}>
              {children}
            </strong>
          ),
          em: ({ children }: JSX.IntrinsicElements["em"]) => (
            <em className={
              custom_css.em_class.length > 0 ? custom_css.em_class : classNames(
                "italic",
                classNameByTheme(theme_color, ["text"], custom_color),
              )
            }>{children}</em>
          ),
          code: ({ children, className }: JSX.IntrinsicElements["code"]) => CodeBlock({ children, className }, theme_color, custom_color, custom_css),
          pre: ({ children }: JSX.IntrinsicElements["pre"]) => {
            return (
              <div className="relative mb-6">
                <pre className={custom_css.pre_class.length > 0 ? custom_css.pre_class : classNames(
                  "p-4 rounded-lg border-2 [&>code.hljs]:p-0 [&>code.hljs]:bg-transparent font-code text-sm overflow-x-auto flex items-start",
                  classNameByTheme(theme_color, ["border", "bg"], custom_color),
                )}>
                  {children}
                </pre>
              </div>
            );
          },
          ul: ({ children }: JSX.IntrinsicElements["ul"]) => (
            <ul className={custom_css.ul_class.length > 0 ? custom_css.ul_class : classNames(
              "flex flex-col gap-3 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3",
              classNameByTheme(theme_color, ["text"], custom_color),
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
            <ol className={custom_css.ol_class.length > 0 ? custom_css.ol_class : classNames(
              "flex flex-col gap-3 my-6 pl-3 [&_ol]:my-3 [&_ul]:my-3",
              classNameByTheme(theme_color, ["text"], custom_color),
            )}>
              {Children.map(
                flattenChildren(children).filter(isValidElement),
                (child, index) => (
                  <li key={index} className="flex gap-2 items-start">
                    <div
                      className={custom_css.li_class.length > 0 ? custom_css.li_class : classNames(
                        "font-sans text-sm font-semibold shrink-0 min-w-[1.4ch]",
                        classNameByTheme(theme_color, ["text"], custom_color),
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
            <div className={
              custom_css.li_class.length > 0 ? custom_css.li_class : classNames(
                "font-sans text-sm",
                classNameByTheme(theme_color, ["text"], custom_color),
              )
            }>{children}</div>
          ),
          table: ({ children }: JSX.IntrinsicElements["table"]) => (
            <div className="overflow-x-auto mb-6">
              <table className={custom_css.table_class.length > 0 ? custom_css.table_class : classNames(
                "table-auto border-2",
                classNameByTheme(theme_color, ["border"], custom_color),
              )}>
                {children}
              </table>
            </div>
          ),
          thead: ({ children }: JSX.IntrinsicElements["thead"]) => (
            <thead className={custom_css.thead_class.length > 0 ? custom_css.thead_class : classNames(
              classNameByTheme(theme_color, ["bg"], custom_color),
            )}>{children}</thead>
          ),
          th: ({ children }: JSX.IntrinsicElements["th"]) => (
            <th className={custom_css.th_class.length > 0 ? custom_css.th_class : classNames(
              "border-2 p-2 font-sans text-sm font-semibold",
              classNameByTheme(theme_color, ["border", "text"], custom_color),
            )}>
              {children}
            </th>
          ),
          td: ({ children }: JSX.IntrinsicElements["td"]) => (
            <td className={custom_css.td_class.length > 0 ? custom_css.td_class : classNames(
              "border-2 p-2 font-sans text-sm",
              classNameByTheme(theme_color, ["border", "text"], custom_color),
            )}>
              {children}
            </td>
          ),
          blockquote: ({ children }: JSX.IntrinsicElements["blockquote"]) => (
            <blockquote className={custom_css.blockquote_class.length > 0 ? custom_css.blockquote_class : classNames(
              "border-l-4 pl-2 italic",
              classNameByTheme(theme_color, ["border", "text"], custom_color),
            )}>
              {children}
            </blockquote>
          ),
        },
      })
      .processSync(content).result;
  }, [content, theme_color]);
};

const CodeBlock = ({ children, className }: JSX.IntrinsicElements["code"], theme_color: ThemeColor = "green", custom_color: CustomColor, custom_css: CustomCSS) => {
  const isMermaid = className ? className.includes("language-mermaid") : false;
  const isLatex = className ? className.includes("language-latex") : false;

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
              <Latex content={children?.toString() ?? ""} theme_color={theme_color} custom_color={custom_color} custom_css={custom_css}/>
            </div>
          ) : (
            showMermaidPreview ? (
              <div className={`flex-grow flex-shrink my-auto`}>
                <Mermaid content={children?.toString() ?? ""} theme_color={theme_color} custom_color={custom_color} custom_css={custom_css}/>
              </div>
            ) : (
              <code ref={ref} className={custom_css.code_class.length > 0 ? custom_css.code_class : `${className} flex-grow flex-shrink my-auto`}>
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
              classNameByTheme(theme_color, ["border", "text", "hover_bg"], custom_color)
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
                className={custom_css.code_button_class.length > 0 ? custom_css.code_button_class : classNames(
                  "rounded-md p-1 border-2 transition-colors",
                  classNameByTheme(theme_color, ["border", "text", "hover_bg"], custom_color)
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
                className={custom_css.code_button_class.length > 0 ? custom_css.code_button_class : classNames(
                  "rounded-md p-1 border-2 transition-colors",
                  classNameByTheme(theme_color, ["border", "text", "hover_bg"], custom_color)
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
    <code className={custom_css.code_class.length > 0 ? custom_css.code_class : classNames(
      "inline-block font-code p-0.5 -my-0.5 rounded",
      classNameByTheme(theme_color, ["text", "bg"], custom_color)
    )}>
      {children}
    </code>
  );
};

const Latex = ({ content, theme_color = "green", custom_color, custom_css }: { content: string, theme_color?: ThemeColor, custom_color: CustomColor, custom_css: CustomCSS }) => {
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
    Streamlit.setFrameHeight()
  }, [content]);

  if (diagram === true) {
    return (
      <div className="flex gap-2 items-center">
        <CircleNotch className={classNames(
          "animate-spin w-4 h-4",
          classNameByTheme(theme_color, ["text"], custom_color)
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
    return <div className={
      custom_css.code_latex_class.length > 0 ? custom_css.code_latex_class : classNames(
        "font-sans text-sm",
        classNameByTheme(theme_color, ["text"], custom_color),
      )
    } dangerouslySetInnerHTML={{ __html: diagram ?? "" }} />;
  }
};

const Mermaid = ({ content, theme_color = "green", custom_color, custom_css }: { content: string, theme_color?: ThemeColor, custom_color: CustomColor, custom_css: CustomCSS }) => {
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
      Streamlit.setFrameHeight()
    };
    render();
  }, [content]);

  if (diagram === true) {
    return (
      <div className="flex gap-2 items-center">
        <CircleNotch className={classNames(
          "animate-spin w-4 h-4",
          classNameByTheme(theme_color, ["text"], custom_color)
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
            classNameByTheme(theme_color, ["text", "hover_text"], custom_color)
          )}
          target="_blank"
        >
          Mermaid Live Editor
        </Link>
        .
      </p>
    );
  } else {
    return <div className={
      custom_css.code_mermaid_class.length > 0 ? custom_css.code_mermaid_class : classNames(
        "font-sans text-sm",
        classNameByTheme(theme_color, ["text"], custom_color),
      )
    } dangerouslySetInnerHTML={{ __html: diagram ?? "" }} />;
  }
};
