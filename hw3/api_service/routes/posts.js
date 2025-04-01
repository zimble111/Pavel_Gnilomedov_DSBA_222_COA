const express = require("express");
const router = express.Router();
const client = require("../grpc/postClient");
const jwt = require("jsonwebtoken");

function auth(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ error: "Unauthorized" });
  try {
    req.user = jwt.verify(token, "supersecretkey");
    next();
  } catch {
    res.status(403).json({ error: "Invalid token" });
  }
}

function postToPlain(post) {
  return {
    id: post.id,
    title: post.title,
    description: post.description,
    creator_id: post.creator_id,
    created_at: post.created_at,
    updated_at: post.updated_at,
    is_private: post.is_private,
    tags: post.tags,
  };
}

router.post("/", auth, (req, res) => {
  const data = {
    ...req.body,
    creator_id: req.user.user_id,
  };

  client.CreatePost(data, (err, response) => {
    if (err) return res.status(500).json({ error: err.message });
    res.status(201).json(postToPlain(response));
  });
});

router.get("/", auth, (req, res) => {
  const { page = 1, page_size = 10 } = req.query;

  client.ListPosts(
    { page: +page, page_size: +page_size, requester_id: req.user.user_id },
    (err, response) => {
      if (err) return res.status(500).json({ error: err.message });

      const posts = response.posts.map(postToPlain);
      res.json({ posts });
    }
  );
});

router.get("/:id", auth, (req, res) => {
  client.GetPost(
    { id: +req.params.id, requester_id: req.user.user_id },
    (err, response) => {
      if (err) return res.status(404).json({ error: err.message });
      res.json(postToPlain(response));
    }
  );
});

router.put("/:id", auth, (req, res) => {
  const data = {
    ...req.body,
    id: +req.params.id,
    updater_id: req.user.user_id,
  };

  client.UpdatePost(data, (err, response) => {
    if (err) return res.status(403).json({ error: err.message });
    res.json(postToPlain(response));
  });
});

router.delete("/:id", auth, (req, res) => {
  client.DeletePost(
    { id: +req.params.id, deleter_id: req.user.user_id },
    (err, response) => {
      if (err) return res.status(403).json({ error: err.message });
      res.status(204).send();
    }
  );
});

module.exports = router;
