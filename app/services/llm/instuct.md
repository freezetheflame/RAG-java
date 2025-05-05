# 涓流输出（Streaming Output）的效果实现
核心在于利用语言模型的流式接口（Stream API）。通过流式接口，模型可以逐步返回生成的内容，而不是等待整个生成过程完成后一次性返回结果。这种模式非常适合实时性要求较高的场景，例如聊天机器人或交互式问答系统。

以下新增一个支持流式输出的接口，附带前端调用的方法。


### **1. 前端调用方法**

为了实现涓流输出效果，前端需要使用 Server-Sent Events (SSE) 来接收逐步生成的内容。以下是两种常见的实现方式：


#### ** 使用 SSE 实现涓流输出**

##### **后端代码**
在后端新增一个 SSE 路由，将流式生成的内容逐步发送给前端。

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from app.services.hunyuan_service import hunyuanService

app = FastAPI()
hunyuan_service = hunyuanService()


@app.get("/sse/stream")
async def sse_stream(request: Request):
    async def event_generator():
        prompt = request.query_params.get("prompt", "")
        async for chunk in hunyuan_service.astream_generate(prompt):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

##### **前端代码**
前端通过 EventSource 连接到后端，并逐步接收生成的内容。

```javascript
const eventSource = new EventSource("/sse/stream?prompt=什么是量子计算？");

eventSource.onmessage = (event) => {
    const chunk = event.data;
    document.getElementById("output").innerText += chunk; // 动态更新页面内容
};

eventSource.onerror = () => {
    console.log("EventSource closed");
    eventSource.close();
};
```

---

### **3. 总结**

- **后端改动**：
  - 新增 `astream_generate` 方法，支持流式生成。
  - 提供  SSE 接口，将流式内容逐步发送到前端。

- **前端实现**：
  - 使用  SSE 动态接收后端返回的内容，并逐步更新页面。

- **优势**：
  - 流式输出显著提升了用户体验，尤其是在生成较长文本时。
  -  SSE 是成熟的实时通信技术，易于实现和扩展。


https://medium.com/@tahsinkheya/server-sent-events-using-python-flask-and-react-js-e564e03b03e9