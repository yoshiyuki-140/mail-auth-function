'use client';

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation";

interface RequestTokenInfo {
    email: string | null,
    token: string | null,
}

interface ResponseBody {
    code: string,
    Message: string,
}

const postTokenInfo = async (url: string, data: RequestTokenInfo): Promise<ResponseBody> => {
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

    const [email, setEmail] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        token: '',
    });


    // 初回レンダリング時にメールアドレスをセッションストレージから取得する
    useEffect(() => {
        // セッションストレージからemailを取得
        const savedEmail = sessionStorage.getItem("email");
        setEmail(savedEmail);
    }, []);


    // フォームの入力欄が変更されたときの処理
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };


    // フォームの入力欄がSubmitされたときの処理
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        // ここにデータの送信処理を書く
        // START
        const url = 'http://localhost:8000/temporary_user/token_auth'; // 送信先のエントリポイントを指定
        const data: RequestTokenInfo = {
            email: email,
            token: formData.token,
        };
        try {
            const response = await postTokenInfo(url, data);
            console.log("Success-register:", response);
            router.push("/success-register");
        } catch (error) {
            console.log("Request failed:", error);
            router.push("/failed-register");
        }
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
                                inputMode="numeric"
                                pattern="[0-9]{6}" // 6桁の数値を指定
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
