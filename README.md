# Xue

$$
35 = 5 \times 7
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

## Tailwind CSS

Tailwind CSS 的 JIT (Just-In-Time) 模式，以下是实现步骤:

1. 安装必要的依赖:

```bash
npm init -y
npm install tailwindcss@latest postcss@latest autoprefixer@latest
```

2. 创建 Tailwind CSS 配置文件:

```bash
npx tailwindcss init -p
```

这将创建 `tailwind.config.js` 和 `postcss.config.js` 文件。

3. 修改 `tailwind.config.js`:

```javascript
module.exports = {
  mode: 'jit',
  purge: [
    './templates/**/*.html',
    './static/**/*.js',
    './your_python_file.py',  // 包含你的 Python 代码的文件
  ],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
```

4. 创建一个 `input.css` 文件:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

5. 添加一个 npm 脚本到 `package.json`:

```json
"scripts": {
  "build-css": "tailwindcss -i ./input.css -o ./static/styles.css --watch"
}
```

6. 运行构建脚本:

```bash
npm run build-css
```

这将启动一个监视进程，每当你的 Python 文件发生变化时，它都会重新生成 CSS。