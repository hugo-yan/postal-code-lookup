# Vercel 部署指南 - 从 0 到 1

## 项目：Postal Code Lookup

---

## 第一步：准备项目代码

### 1.1 初始化 Git 仓库

在项目根目录打开 PowerShell，执行：

```bash
# 进入项目目录
cd "D:\4.Other file\trae dome\shijieyoubian"

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Postal Code Lookup website"
```

### 1.2 创建 GitHub 仓库

1. 访问 [github.com](https://github.com)
2. 登录你的账号（没有就注册）
3. 点击右上角 **+** → **New repository**
4. 填写信息：
   - Repository name: `postal-code-lookup`
   - Description: `Free postal code and zip code lookup for 40+ countries`
   - 选择 **Public**（免费）
   - 不要勾选 "Add a README file"
5. 点击 **Create repository**

### 1.3 推送代码到 GitHub

```bash
# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/postal-code-lookup.git

# 推送代码
git push -u origin main

# 如果提示输入用户名密码，输入你的 GitHub 账号和密码
```

---

## 第二步：注册 Vercel 账号

### 2.1 访问 Vercel

1. 打开 [vercel.com](https://vercel.com)
2. 点击 **Sign Up**
3. 选择 **Continue with GitHub**
4. 授权 Vercel 访问你的 GitHub 账号

### 2.2 验证邮箱

- 检查邮箱，点击验证链接
- 完成注册

---

## 第三步：部署网站到 Vercel

### 3.1 导入项目

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 **Add New Project**
3. 在 "Import Git Repository" 下找到你的 `postal-code-lookup` 仓库
4. 点击 **Import**

### 3.2 配置项目

在配置页面：

| 配置项 | 设置值 | 说明 |
|--------|--------|------|
| Framework Preset | **Other** | 纯 HTML 网站 |
| Root Directory | `./` | 根目录 |
| Build Command | 留空 | 不需要构建 |
| Output Directory | 留空 | 默认即可 |

点击 **Deploy**

### 3.3 等待部署完成

- 部署过程约 1-2 分钟
- 完成后会显示：**Congratulations!** 
- 获得临时域名：`https://postal-code-lookup-你的用户名.vercel.app`

### 3.4 测试访问

点击 Vercel 提供的链接，确认网站正常显示。

---

## 第四步：绑定自定义域名 `postalcodelookup.info`

### 4.1 在 Vercel 添加域名

1. 进入 Vercel Dashboard
2. 点击你的项目 `postal-code-lookup`
3. 点击顶部 **Settings** 标签
4. 左侧选择 **Domains**
5. 在输入框输入：`postalcodelookup.info`
6. 点击 **Add**

Vercel 会显示需要配置的 DNS 记录：

```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### 4.2 在阿里云配置 DNS

1. 登录 [阿里云控制台](https://www.aliyun.com)
2. 进入 **域名解析** 服务
3. 找到你的域名 `postalcodelookup.info`
4. 点击 **解析设置**
5. 添加以下记录：

**记录 1：**
```
记录类型：A
主机记录：@
解析线路：默认
记录值：76.76.21.21
TTL：600
```

**记录 2：**
```
记录类型：CNAME
主机记录：www
解析线路：默认
记录值：cname.vercel-dns.com
TTL：600
```

6. 点击 **确认**

### 4.3 等待 DNS 生效

- 通常 5 分钟 - 48 小时
- 可以用 [whatsmydns.net](https://whatsmydns.net) 检查全球解析状态

### 4.4 在 Vercel 验证域名

1. 回到 Vercel → 你的项目 → Settings → Domains
2. 点击域名旁边的 **Verify** 按钮
3. Vercel 会自动配置 HTTPS 证书
4. 状态变为 **Valid Configuration** ✅

---

## 第五步：配置 HTTPS（自动完成）

Vercel 会自动：
- ✅ 申请 Let's Encrypt SSL 证书
- ✅ 自动续期
- ✅ 强制 HTTPS 跳转

无需手动操作！

---

## 第六步：验证部署

### 6.1 检查清单

- [ ] 访问 `https://postalcodelookup.info` 正常显示
- [ ] 访问 `https://www.postalcodelookup.info` 正常显示
- [ ] 访问 `https://postalcodelookup.info/sitemap.xml` 可访问
- [ ] 访问 `https://postalcodelookup.info/robots.txt` 可访问
- [ ] 浏览器显示锁图标（HTTPS 生效）

### 6.2 测试几个页面

- [ ] 首页：`https://postalcodelookup.info`
- [ ] 国家页：`https://postalcodelookup.info/country.html?country=US`
- [ ] 博客页：`https://postalcodelookup.info/blog.html`

---

## 第七步：提交 Google Search Console

### 7.1 注册 Search Console

1. 访问 [search.google.com/search-console](https://search.google.com/search-console)
2. 用 Google 账号登录
3. 选择 **网址前缀**，输入：`https://postalcodelookup.info/`
4. 点击 **继续**

### 7.2 验证网站所有权

**推荐方法：HTML 文件验证**

1. 下载 Google 提供的 HTML 验证文件
2. 放到项目根目录
3. 提交到 GitHub：

```bash
git add .
git commit -m "Add Google Search Console verification"
git push
```

4. Vercel 会自动重新部署
5. 点击验证

### 7.3 提交 Sitemap

1. 在 Search Console 左侧菜单点击 **Sitemap**
2. 输入：`sitemap.xml`
3. 点击 **提交**

---

## 第八步：后续更新网站

### 8.1 修改代码后重新部署

```bash
# 修改代码后
git add .
git commit -m "Update: 描述你的修改"
git push

# Vercel 会自动重新部署！
```

### 8.2 查看部署状态

- 访问 [Vercel Dashboard](https://vercel.com/dashboard)
- 点击项目查看部署历史

---

## 常见问题

### Q: 部署失败怎么办？

**检查：**
1. 项目根目录是否有 `index.html`
2. 文件路径是否正确
3. GitHub 仓库是否公开

### Q: 域名解析不生效？

**解决：**
1. 检查 DNS 记录是否正确
2. 等待 24-48 小时
3. 清除本地 DNS 缓存：`ipconfig /flushdns`

### Q: 如何设置环境变量？

**步骤：**
1. Vercel Dashboard → 项目 → Settings → Environment Variables
2. 添加变量名和值
3. 重新部署

### Q: 免费版有什么限制？

| 限制项 | 免费版额度 |
|--------|-----------|
| 带宽 | 100GB/月 |
| 构建时间 | 6000 分钟/月 |
| 并发构建 | 1 个 |
| 团队成员 | 1 人 |
| 自定义域名 | 支持 |

**对于你的网站完全够用！**

---

## 部署完成！🎉

你的网站现在：
- ✅ 部署在全球 CDN 上
- ✅ 有自定义域名
- ✅ 自动 HTTPS
- ✅ 自动部署
- ✅ 已提交 Google

下一步：
1. 申请 Google AdSense
2. 添加联盟营销链接
3. 持续更新博客内容

---

## 快速命令参考

```bash
# 日常更新
git add .
git commit -m "描述修改"
git push

# 查看状态
git status

# 查看日志
git log --oneline
```

---

**祝你网站成功上线！** 🚀
