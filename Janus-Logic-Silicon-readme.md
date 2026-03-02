# Janus-Logic-Silicon-readme

**「项目本质 (Essence)」**。

> "JLS is not a website, it's a gateway to a Cognitive OS. The UI must feel like a 1980s logic terminal. Silence is better than noise. Precision is better than decoration."

**Context Anchor:** 你正在协助 Architect-Seven 构建 `JANUS-LOGIC-SILICON` 系列产品的数字孪生系统。

 **Project Goal:** 构建一个极简、硬核、单页面的 H5 Landing Page，用于物理卡片的唯一码校验与逻辑固件（LISP 代码）的分发。

#### 1. 技术栈要求 (Tech Stack)

- **Frontend:** 原生 HTML5 / CSS3 (Terminal Style) / Vanilla JS。
- **Backend:** Supabase (Auth + Database + RLS)。
- **Design Language:** "Obsidian Logic" (黑底、荧光绿 #39FF14、高对比度、扫描线动效)。
- **Logic:** LISP-Dehydrated Mind Models

#### 2. 核心模块逻辑 (Module Logic)

- **Module_03 (Decoder):** 12位唯一码输入（XXXX-XXXX-XXXX格式化）。
- **Module_04 (Bridge):** 调用 Supabase API 校验 `redeem_code` 状态。
- **Module_05 (Manual):** 展示 M5W LISP 核心代码，支持一键复制。

#### 3. 数据库 Schema 参考 (Supabase)

需要在 Supabase 中预设表 `logic_cartridges`:

- `redeem_code` (text, primary key)
- `status` (boolean, default: false)
- `model_id` (text, e.g., 'M5W')
- `claimed_at` (timestamptz)

#### 4. 视觉资产描述 (Visual Assets)

- **Font:** 'Courier New', monospace.
- **Effect:** 背景需有 2px 间隔的半透明扫描线 (Scanlines)。
- **Vibe:** 模拟 80 年代逻辑终端，禁止使用现代圆角 UI。