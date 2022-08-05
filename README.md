## LibreTorrent Source Code
### About
This is the source code for [libretorrent.com](http://libretorrent.com)

### Usage
#### Development
Generate `index.html`
```bash
make build
```

Upload to s3 (requries [aws cli profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) named `libretorrent`)
```bash
make upload
```

Generate + upload
```bash
make release
```

#### Testing
Build and open `index.html` locally
```bash
make local
```