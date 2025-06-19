FROM golang:1.22-alpine

WORKDIR /app

# Copy go.mod and go.sum first for better caching and dependency resolution
COPY go.mod ./
COPY go.sum ./  
# if you don't have this yet, you can skip this line temporarily

RUN go mod download

# Now copy the rest of your source code
COPY . .

# Build the app
RUN go build -o aws-worker ./cmd/main.go

# Set entry point
CMD ["./aws-worker"]
