// console.log("eye.js loaded");
// デバッグ目的の目印
// このJSが読み込まれたかを確認するために一時的に入れたコード

document.addEventListener("DOMContentLoaded", () => {
// HTMLが全部読み込まれてから中のJSを実行してねという命令
    document.querySelectorAll(".toggle-password").forEach(button => {
        // document:Webページ全体(HTML全部)を指すもの
        // querySelectorAll(".toggle-password"):classがtoggle-passwordの要素を全部集める
        // .はclassの意味
        // つまり目ん玉ボタン(toggle-password)を全部拾ってくる
        // forEach(button => {...}):拾ったボタンのリストを1個ずつ順番に処理するためのもの
        button.addEventListener("click", () => {
            // addEventListener:イベント(操作)が起きたら処理する仕組み
            // "click":クリックされたら
            // () => {...}:クリックされた時に実行する処理(関数)
            // つまり、このボタンが押されたら、中の処理を動かす
            
            // console.log("eye clicked");
            // クリックが動作しているか確認するために一時的に入れたコード

            const targetId = button.getAttribute("data-target");
            // const:定数を宣言するキーワード
            // 書き方：const 変数名　= 値；
            // getAttribute("data-target"):HTMLのdata-target="..."の値を取ってくる
            // つまり、このボタンが操作するinputのIDを取得
            
            const input = document.getElementById(targetId);
            // getElementById():指定したIDの要素を１個取ってくる
            // さっき取ったtargetIdを使って入力欄を取得
            // つまりパスワード入力欄そのもの(inputタグ)を取得
            if (!input) return;
            // i:真偽値に変換して反対の真偽値を取得
            // if (!input)　は if (input ===null)と同じ意味
            // つまり対応するinputが見つからなかったら、これ以上処理せず終わる
            
            const icon = button.querySelector("i");
            // ボタンの中にある<i ...>を探して取る
            // HTMLの<i class="bi bi-eye-slash"></i>👁️を取得(目のアイコン)
            
            // ここからが切り替え処理
            if (input.type === "password"){
                // 演算子　===:値と型が等しいことを確認
                input.type = "text";
                // input.type = "text"：パスワードを表示する
                
                // 👁️アイコンの切り替え
                icon.classList.remove("bi-eye-slash");
                // classList: classを操作するためのもの
                // remove(): そのclassを消す
                // bi-eye-slash:閉じ目
                icon.classList.add("bi-eye");
                // add():そのclassを付ける
                // bi-eye:開き目
            } else {
                input.type = "password";
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            }          
        });
    });
});

