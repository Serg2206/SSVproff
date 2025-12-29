import type { NextPage } from 'next';
import Head from 'next/head';

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>SSV Prof Platform</title>
        <meta name="description" content="SSV Prof Platform - Web Client" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <h1>Welcome to SSV Prof Platform</h1>
        <p>Web client powered by Next.js and React</p>
      </main>
    </>
  );
};

export default Home;
