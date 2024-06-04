import type { NextPage } from "next";
import Head from "next/head";
import { StreamlitProvider } from "streamlit-component-lib-react-hooks";
import StreamlitMarkdown from "@/components/streamlit-markdown";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <StreamlitProvider>
        <StreamlitMarkdown />
      </StreamlitProvider>
    </>
  );
};

export default Home;