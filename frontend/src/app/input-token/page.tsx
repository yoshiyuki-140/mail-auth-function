'use client';

import { useState } from "react"

export default function Home() {
    const [formData, setFormData] = useState({
        token: '',
    });

    // フォームの入力欄が変更されたときの処理
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // フォームの入力欄がSubmitされたときの処理
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        // ここにデータの送信処理を書く
        // START
        console.log(formData); // データ送信の処理（API経由など）
        // END
    }


    return (
        <div className="flex items-center justify-center h-screen w-screen bg-white">
            <div className="text-white p-4 w-11/12 flex flex-col items-center">
                <div className="mb-6 text-center">
                    <h1 className="text-black text-3xl font-semibold">メール認証</h1>
                </div>
                <div className="flex items-center justify-center w-full">
                    <form
                        onSubmit={handleSubmit}
                        className="bg-blue-300 p-6 rounded shadow-md w-full max-w-md text-black flex flex-col items-center"
                    >
                        <strong>
                            <p>ご登録いただいたメールアドレス宛に、6桁のトークンを送信しました。確認の上、下部入力欄に入力ください。</p>
                        </strong>
                        <br />
                        <div className="flex flex-col w-full">
                            <input
                                type="text"
                                name="token"
                                maxLength={6}
                                inputMode="numeric"
                                pattern="[0-9]"
                                placeholder="トークン6桁"
                                value={formData.token}
                                onChange={handleChange}
                                className="w-full p-2 mb-4 border border-black rounded"
                                required
                            />

                            <button
                                type="submit"
                                className="shadow-lg w-28 bg-red-500 hover:bg-red-400 text-black p-2 border border-black rounded-full mx-auto mt-4"
                            >
                                認証
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
