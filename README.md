# 🔥 Daily Hots

基于 Model Context Protocol (MCP) 协议的全网热点趋势一站式聚合服务 - Python实现

## ✨ 特性

- 📊 **一站式聚合** - 聚合全网热点资讯，覆盖30个优质数据源
- 🔄 **实时更新** - 保持与源站同步的最新热点数据
- 🧩 **MCP 协议支持** - 完全兼容 Model Context Protocol，轻松集成到 AI 应用
- 🔌 **易于扩展** - 简单配置即可添加自定义数据源
- 🎨 **灵活定制** - 通过环境变量轻松调整返回字段
- 🐍 **Python实现** - 使用Python开发，更好的可维护性和扩展性
- 🌐 **多领域覆盖** - 新闻资讯、社交媒体、科技开发、财经投资、汽车、生活消费等

## 📦 安装

### 方式一：从源码安装

```bash
git clone https://github.com/fancyboi999/daily-hot-mcp.git
cd daily-hot-mcp
pip install -r requirements.txt
pip install -e .
```

## 📖 使用指南

### 配置环境变量

首先复制环境变量模板文件：

```bash
cp env.example .env
```

#### 自定义配置选项

##### `TRENDS_HUB_CUSTOM_RSS_URL` - 自定义 RSS 订阅源

支持通过环境变量添加自定义 RSS 源：

```bash
TRENDS_HUB_CUSTOM_RSS_URL=https://your-rss-feed-url.com/feed
```

配置后系统将自动添加 `custom-rss` 工具，用于获取指定的 RSS 订阅源内容。

##### `FIRECRAWL_API_KEY` - 爬虫服务 API 密钥

用于获取热点内容的详细信息：

```bash
FIRECRAWL_API_KEY=your_api_key_here
```

此配置允许系统抓取目标热点的完整内容，提供更丰富的信息展示。API 密钥可在 [FireCrawl官网](https://www.firecrawl.dev/app) 申请获取。

### 命令行运行

```bash

# 直接运行模块
python daily_hot_mcp/__main__.py
```

### MCP客户端配置

#### JSON 配置

```json
{
  "mcpServers": {
    "daily-news": {
      "type": "http",
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

## 🛠️ 支持的工具 (30个)

### 📰 新闻资讯类 (11个)

| 工具名称 | 描述 |
| --- | --- |
| get-baidu-trending | 获取百度热榜，包含实时热搜、社会热点、科技新闻、娱乐八卦等多领域的热门中文资讯和搜索趋势 |
| get-toutiao-trending | 获取今日头条热榜，包含时政要闻、社会事件、国际新闻、科技发展及娱乐八卦等多领域的热门中文资讯 |
| get-ithome-trending | 获取IT之家热榜，包含科技资讯、数码产品、互联网动态、软件应用及前沿科技发展的热门中文科技新闻 |
| get-bbc-news | 获取 BBC 新闻，提供全球新闻、英国新闻、商业、政治、健康、教育、科技、娱乐等资讯 |
| get-36kr-trending | 获取 36 氪热榜，提供创业、商业、科技领域的热门资讯，包含投融资动态、新兴产业分析和商业模式创新信息 |
| get-netease-news-trending | 获取网易新闻热点榜，包含时政要闻、社会事件、财经资讯、科技动态及娱乐体育的全方位中文新闻资讯 |
| get-infoq-news | 获取 InfoQ 技术资讯，包含软件开发、架构设计、云计算、AI等企业级技术内容和前沿开发者动态 |
| get-thepaper-trending | 获取澎湃新闻热榜，包含时政要闻、财经动态、社会事件、文化教育及深度报道的高质量中文新闻资讯 |
| get-tencent-news-trending | 获取腾讯新闻热点榜，包含国内外时事、社会热点、财经资讯、娱乐动态及体育赛事的综合性中文新闻资讯 |
| get-theverge-news | 获取 The Verge 新闻，包含科技创新、数码产品评测、互联网趋势及科技公司动态的英文科技资讯 |
| get-9to5mac-news | 获取 9to5Mac 苹果相关新闻，包含苹果产品发布、iOS 更新、Mac 硬件、应用推荐及苹果公司动态的英文资讯 |

### 📱 社交媒体热榜类 (9个)

| 工具名称 | 描述 |
| --- | --- |
| get-kuaishou-trending | 获取快手热榜，包含快手平台的热门短视频、热点话题及流行内容的实时热门中文资讯 |
| get-xiaohongshu-trending | 获取小红书热榜，包含小红书平台的热门笔记、时尚美妆、生活方式、种草推荐等热门中文内容 |
| get-so360-trending | 获取360热搜榜，包含360搜索平台的热门搜索词、实时新闻热点及用户关注度较高的中文资讯 |
| get-sogou-trending | 获取搜狗热搜榜，包含搜狗搜索平台的热门搜索关键词、实时搜索趋势及用户关注的热点中文资讯 |
| get-hupu-trending | 获取虎扑热榜，包含虎扑体育赛事、步行街热帖、篮球足球话题及男性生活兴趣的热门中文讨论内容 |
| get-weibo-trending | 获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯 |
| get-zhihu-trending | 获取知乎热榜，包含时事热点、社会话题、科技动态、娱乐八卦等多领域的热门问答和讨论的中文资讯 |
| get-douyin-trending | 获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势 |
| get-bilibili-trending | 获取哔哩哔哩热门视频 |

### 🎮 娱乐与内容平台 (4个)

| 工具名称 | 描述 |
| --- | --- |
| get-bilibili-rank | 获取哔哩哔哩视频排行榜，包含全站、动画、音乐、游戏等多个分区的热门视频，反映当下年轻人的内容消费趋势 |
| get-douban-rank | 获取豆瓣实时热门榜单，提供当前热门的图书、电影、电视剧、综艺等作品信息，包含评分和热度数据 |
| get-weread-rank | 获取微信读书排行榜，包含热门小说、畅销书籍、新书推荐及各类文学作品的阅读数据和排名信息 |
| get-gcores-new | 获取机核网游戏相关资讯，包含电子游戏评测、玩家文化、游戏开发和游戏周边产品的深度内容 |

### 🚗 汽车类 (1个)

| 工具名称 | 描述 |
| --- | --- |
| get-autohome-trending | 获取汽车之家热榜，包含汽车新闻、新车发布、购车指南、试驾体验、汽车评测及汽车行业动态的专业汽车资讯 |

### 🛒 生活消费类 (3个)

| 工具名称 | 描述 |
| --- | --- |
| custom-rss | 自定义RSS订阅源: your_url_here |
| get-smzdm-rank | 获取什么值得买热门，包含商品推荐、优惠信息、购物攻略、产品评测及消费经验分享的实用中文消费类资讯 |
| get-sspai-rank | 获取少数派热榜，包含数码产品评测、软件应用推荐、生活方式指南及效率工作技巧的优质中文科技生活类内容 |

### 🌐 其他工具 (2个)

| 工具名称 | 描述 |
| --- | --- |
| crawl_website | 爬取网站内容，多用于用户想要详细了解某网站内容时使用 |
| get-ifanr-news | 获取爱范儿科技快讯，包含最新的科技产品、数码设备、互联网动态等前沿科技资讯 |

> 💡 **提示**: 更多数据源正在持续增加中，我们致力于为您提供最全面的热点趋势信息！

## 📄 许可证

MIT License

## 🙏 鸣谢

- [DailyHotApi](https://github.com/imsyy/DailyHotApi) - 提供了优秀的热榜API设计思路
- [RSSHub](https://github.com/DIYgod/RSSHub) - RSS聚合服务的灵感来源
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP协议规范
- 感谢所有贡献者和用户的支持与反馈

---

**🎯 打造最全面的中文热点趋势聚合服务，让信息触手可及！** 