<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <h1><center>Glb2Ply</center></h1>
        <h2>なにものか？</h2>
        <p>
          ・Depth Anything v3 の WEBデモなど, RGB画像から奥行き推定や3D化をした結果は glbでしかダウンロードできない。<br>
          ・glb の点群に RGB情報が見当たらなかったため, 点群に元のRGB画像の色情報を付加してみた。<br>
          　(多分探せば良いツールがいくらでもありそうだけど･･･)<br>
          ・glb/glTF の仕様書を確認していない適当な実装。<br>
            <br>
            <img src="images/glb2ply.svg">
        </p>
        <h2>環境構築方法</h2>
        <p>
            pip install opencv-python open3d trimesh
        </p>
        <h2>使い方</h2>
        <p>
           ● GLBファイルにRGB情報を付加してPLYファイルとして書き出す。<br>
　　           python glb2ply.py  (RGB画像ファイル)  (glbファイル)  [(zスケール)]<br>
<br>
           ● PLYファイルの確認方法<br>       
               python o3d_display_ply.py (plyファイル)<br>

　　　　　　 <table border="1">
                <tr><th>操作</th><th>機能</th></tr>
                <tr><td>左ボタン押下＋ドラッグ</td><td>3Dモデルの回転</td></tr>
                <tr><td>ホイールボタン押下＋ドラッグ</td><td>3Dモデルの移動</td></tr>
                <tr><td>ホイール回転</td><td>3Dモデルの拡大・縮小</td></tr>
                <tr><td>PrintScreenキー押下</td><td>スクリーンショット保存</td></tr>
                <tr><td>ESCキー押下 または ウィンドウ閉じるボタン押下　</td><td>プログラム終了</td></tr>
            </table>

            ● 点群PLYのメッシュ化<br>
            　python o3d_pcd_to_mesh.py (plyファイル)<br>
        </p>
        <h2>備忘録</h2>
        <p>
        ・GLBファイルにはオブジェクトの点群とカメラの点群が格納されていた。<br>
        ・カメラの点群は, 16個の(x,y,z)座標。<br>
        ・カメラパラメータかと思ったが, それっぽい値(0や1)が全くなく、カメラの視錐体(ピラミッド)と想定。<br>
        ・ピラミッドの頂点なら5点で良いがなぜ16個もデータがある？<br>
        ・データを見るとユニークな座標は5種類。<br>
        　→ ピラミッドの辺は8個 <br>
        　→ 始点と終点で16個格納されていると想像。<br>
         <img src="images/glb2ply2.svg"><br>
         ・上図の配置を想定。<br>
         ・z 座標が一番大きい点を p<sub>0</sub> としてオブジェクトの各点と p<sub>0</sub> を結ぶ直線と
面 p<sub>1</sub>p<sub>2</sub>p<sub>4</sub>p<sub>3</sub> の交点の座標のRGB画像の色を点群に付加した。
        </p>
    </body>
</html>
