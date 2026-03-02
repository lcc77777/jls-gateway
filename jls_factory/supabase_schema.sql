-- ==========================================
-- JLS SCHEMA UPGRADE: MODELS & INVENTORY
-- ==========================================

-- 1. 创建型号注册表 (存储固件母本)
CREATE TABLE IF NOT EXISTS public.models_registry (
    model_id text PRIMARY KEY,      -- 如 M5W-LOGIC
    name text NOT NULL,             -- 型号名称
    category text,                  -- 分类: M-Series, V-Series
    lisp_code text NOT NULL,        -- Base64 编码后的 LISP 固件
    initial_fuel int DEFAULT 1000,  -- 激活奖励
    created_at timestamptz DEFAULT now()
);

-- 2. 优化激活码清单表
-- 如果 logic_inventory 已存在，我们添加外键关联
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'fk_model' AND table_name = 'logic_inventory'
    ) THEN
        ALTER TABLE public.logic_inventory 
        ADD CONSTRAINT fk_model 
        FOREIGN KEY (model_id) 
        REFERENCES public.models_registry(model_id);
    END IF;
END $$;

-- 3. 安全策略 (RLS)
ALTER TABLE public.models_registry ENABLE ROW LEVEL SECURITY;

-- 允许匿名读取固件库
DROP POLICY IF EXISTS "Enable read for all" ON public.models_registry;
CREATE POLICY "Enable read for all" ON public.models_registry
    FOR SELECT USING (true);

-- 4. 索引优化 (加速查询)
CREATE INDEX IF NOT EXISTS idx_logic_inventory_id ON public.logic_inventory (id);

-- 5. 交易对账表 (记录每一笔逻辑燃料的注入)
CREATE TABLE IF NOT EXISTS public.transactions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code_id text NOT NULL,          -- 激活码 ID
    user_handle text,               -- 用户账号/备注
    model_id text,                  -- 卡带型号
    fuel_amount int,                -- 注入数量
    status text DEFAULT 'PENDING',  -- 状态: PENDING (等待 Leo 充值), COMPLETED
    created_at timestamptz DEFAULT now()
);

-- 只允许匿名插入，Leo 手动在后台查看
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable insert for all" ON public.transactions
    FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable read for service role only" ON public.transactions
    FOR SELECT USING (false); -- 匿名不可读，加强安全性
