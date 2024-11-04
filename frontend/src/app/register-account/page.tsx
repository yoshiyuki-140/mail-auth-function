'use client';

import { useState } from "react"
import { useRouter } from "next/navigation";

interface RequestUserInfo {
  name: string,
  email: string,
  password: string,
};

interface ResponseBody {
  Success: string,
}

const postUserInfo = async (url: string, data: RequestUserInfo): Promise<ResponseBody> => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error("HTTP error! Status: ${response.status}");
    }
    const result: ResponseBody = await response.json();
    return result;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export default function Home() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    password_confirm: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // ここにpasswordとpassword_confirmの整合チェックを書く
    if (formData.password != formData.password_confirm) {
      alert("Passwords do not match.") // 警告メッセージ
      return; // 以降の処理をスキップ
    }


    const url = 'http://localhost:8000/temporary_user';
    // ここにデータの送信処理を書く
    // START
    const data: RequestUserInfo = {
      name: formData.name,
      email: formData.email,
      password: formData.password,
    };

    try {
      const response = await postUserInfo(url, data);
      router.push("/input-token");
      console.log("Success:", response);
    } catch (error) {
      console.log("Request failed:", error);
    };
    console.log(formData); // データ送信の処理（API経由など）
    // END

    // 画面遷移処理

  };


  return (
    <div className="flex items-center justify-center h-screen w-screen bg-white">
      <div className="text-white p-4 w-11/12 flex flex-col items-center">
        <div className="mb-6 text-center">
          <h1 className="text-black text-3xl font-semibold">アカウント登録</h1>
        </div>
        <div className="flex items-center justify-center w-full">
          <form
            onSubmit={handleSubmit}
            className="bg-blue-300 p-6 rounded shadow-md w-full max-w-md text-black flex flex-col items-center"
          >
            <div className="flex flex-col w-full">
              <input
                type="text"
                name="name"
                placeholder="ユーザー名"
                value={formData.name}
                onChange={handleChange}
                className="w-full p-2 mb-4 border border-black rounded"
                required
              />

              <input
                type="email"
                name="email"
                placeholder="メールアドレス"
                value={formData.email}
                onChange={handleChange}
                className="w-full p-2 mb-4 border border-black rounded"
                required
              />

              <input
                type="password"
                name="password"
                placeholder="パスワード"
                value={formData.password}
                onChange={handleChange}
                className="w-full p-2 mb-4 border border-black rounded"
                required
              />

              <input
                type="password"
                name="password_confirm"
                placeholder="パスワード確認用"
                value={formData.password_confirm}
                onChange={handleChange}
                className="w-full p-2 mb-4 border border-black rounded"
                required
              />

              <button
                type="submit"
                className="shadow-lg w-28 bg-red-500 hover:bg-red-400 text-black p-2 border border-black rounded-full mx-auto mt-4"
              >
                送信
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
