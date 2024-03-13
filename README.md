# Docker运行监控

## 监听容器运行时事件，执行自定义脚本
#### 1. 支持多容器，多事件同时监听
#### 2. 支持所有docker事件：attach commit copy create destroy detach die exec_create exec_detach exec_die exec_start export health_status kill oom pause rename resize restart start stop top unpause update
#### 3. 支持自定义脚本，建议.sh，将跳过脚本执行中的新事件

## 一、配置文件
1. 下载[config.simple.yaml](https://raw.githubusercontent.com/zhu0823/DockerListener/master/config.simple.yaml)
2. 修改文件名为:config.yaml
3. 移动到:/config/config.yaml
```
containers:
  - name: get-start             #监听的容器名称
    events:
      start: /scripts/start.sh  # 监听docker事件名：执行脚本路径
      stop: /scripts/stop.sh    # 监听docker事件名：执行脚本路径
  - name: get-start-2
    events:
      start: /scripts/start.sh
```
## 二、放置脚本
- 将脚本文件全都放在/scripts目录下\
tip: 目录执行前会修改权限为777

## 三、挂载目录
- ./config:/config
- ./scripts:/scripts
- /var/run/docker.sock:/var/run/docker.sock

## 四、运行
```
docker run -d --name docker-listener \
-v ./config:/config \
-v ./scripts:/scripts \
-v /var/run/docker.sock:/var/run/docker.sock \
zhu0823/docker-listener:latest
```

TODO
- [x] 监听容器事件
- [x] 执行自定义脚本
- [ ] 多容器并行执行脚本
