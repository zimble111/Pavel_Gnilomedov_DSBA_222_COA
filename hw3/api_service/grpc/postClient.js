const path = require("path");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const PROTO_PATH = path.join(__dirname, "../posts.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const postProto = grpc.loadPackageDefinition(packageDefinition).post;

module.exports = new postProto.PostService(
  "post-service:50051",
  grpc.credentials.createInsecure()
);
