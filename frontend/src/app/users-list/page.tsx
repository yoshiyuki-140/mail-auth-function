'use client';

import { useState, useEffect } from "react";

export default function AccountList() {
  const [users, setUsers] = useState<{ name: string }[]>([]);

  useEffect(() => {
    // 非同期関数を定義してデータを取得
    // 取得できるデータの形式は以下のような形
    // {"users":[{"name":"kuro"},{"name":"taro"}]}
    const fetchUsers = async () => {
      try {
        const response = await fetch('/api/users');  // 実際のAPIエンドポイントに置き換えてください
        const data = await response.json();
        setUsers(data.users);
      } catch (error) {
        console.error("データの取得に失敗しました:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="flex items-center justify-center h-screen w-screen bg-white">
      <div className="text-black p-4 w-11/12 flex flex-col items-center">
        <div className="mb-6 text-center">
          <h1 className="text-black text-3xl font-semibold">登録アカウント一覧</h1>
        </div>
        <div className="bg-blue-300 p-6 rounded shadow-md w-full max-w-md text-black">
          {users.length > 0 ? (
            <ul className="space-y-4">
              {users.map((user, index) => (
                <li key={index} className="p-2 border border-black rounded">
                  {user.name}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-center">登録されたアカウントはありません</p>
          )}
        </div>
      </div>
    </div>
  );
}
