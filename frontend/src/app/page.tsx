'use client';

import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();

  const handleNavigation = () => {
    router.push("遷移先のパス");
  }
  return (
    <div className="flex items-center justify-center h-screen w-screen bg-white">
      <div className="text-white p-4 h-screen flex flex-col">
        <div className="mt-20">
          <h1
            className="text-black text-4xl"
          >認証システムデモへようこそ</h1>
        </div>
        <div className="flex justify-center mt-40">
          <button
            onClick={handleNavigation}
            className="text-black border bg-red-500 px-8 py-2 shadow-lg rounded-3xl hover:bg-red-400"
          >
            登録
          </button>
        </div>
      </div>
    </div>
  );
}
