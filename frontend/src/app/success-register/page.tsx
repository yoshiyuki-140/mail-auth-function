import Link from "next/link";

export default function Home() {
  return (
    <div className="flex items-center justify-center h-screen w-screen bg-white">
      <div className="text-black p-4 flex flex-col items-center h-screen">
        <div className="mt-20 text-center space-y-2">
          <p className="font-semibold text-lg">登録完了いたしました〜！</p>
          <p className="font-semibold text-lg">今後ともよろしくお願い致します。</p>
        </div>
        <div className="flex justify-center mt-40">
          <Link
            href="/register-account"
            className="text-black border border-black bg-red-500 px-8 py-2 shadow-lg rounded-3xl hover:bg-red-400"
          >
            サービス開始
          </Link>
        </div>
      </div>
    </div>
  );
}
