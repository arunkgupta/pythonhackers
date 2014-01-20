import uuid
from cqlengine import columns
from cqlengine.models import Model
from datetime import datetime as dt


class MBase(Model):
    __abstract__ = True
    #__keyspace__ = model_keyspace


class PostCounter(MBase):
    id = columns.BigInt(index=True, primary_key=True)
    up_votes = columns.Counter()
    down_votes = columns.Counter()
    views = columns.Counter()
    karma = columns.Counter()
    replies = columns.Counter()


class Post(MBase):
    id = columns.BigInt(index=True, primary_key=True)
    user_id = columns.Integer(required=True, index=True, partition_key=True)
    user_nick = columns.Text()
    text = columns.Text(required=True)
    html = columns.Text(required=False)

    reply_to_id = columns.BigInt()
    reply_to_uid = columns.Integer()
    reply_to_nick = columns.Text()

    ext_id = columns.Text()

    has_url = columns.Boolean()
    has_channel = columns.Boolean()

    # this post is either linked to a
    # DISCUSSION or
    discussion_id = columns.BigInt()
    # CHANNEL or None
    channel_id = columns.Integer()

    spam = columns.Boolean(default=False)
    flagged = columns.Boolean(default=False)
    deleted = columns.Boolean(default=False)

    published_at = columns.DateTime(default=dt.utcnow())

    def to_dict(self):
        return {'id': self.id,
                'text': self.text,
                'html': self.html,
                'user_id': self.user_id,
                'user_nick': self.user_nick,
                'reply_to_id': self.reply_to_id,
                'reply_to_uid': self.reply_to_uid,
                'reply_to_nick': self.reply_to_nick,
                'discussion_id': self.discussion_id,
                'channel_id': self.channel_id,
                'spam': self.spam,
                'flagged': self.flagged,
                'deleted': self.deleted,
                'published_at': self.published_at}


class Project(MBase):
    id = columns.Integer(primary_key=True)
    name = columns.Text()

    #follower_count = columns.Counter


class TopicCounter(MBase):
    id = columns.Integer(primary_key=True)
    views = columns.Counter()
    discussions = columns.Counter()
    messages = columns.Counter()


class Topic(MBase):
    id = columns.Integer(primary_key=True)
    slug = columns.Text()
    name = columns.Text()
    description = columns.Text()
    last_message_id = columns.BigInt(required=False)
    last_message_time = columns.DateTime(default=dt.utcnow())
    main_topic = columns.Boolean(default=False)
    parent_topic = columns.Integer(required=False)
    subtopics = columns.Set(value_type=columns.Integer)


class TopicDiscussion(MBase):
    topic_id = columns.Integer(primary_key=True, required=False)
    discussion_id = columns.BigInt(primary_key=True, required=False)


class Channel(MBase):
    id = columns.Integer(primary_key=True)
    slug = columns.Text(required=True, index=True)
    name = columns.Text(required=True)


class UserCounter(MBase):
    id = columns.Integer(primary_key=True)
    follower_count = columns.Counter()
    following_count = columns.Counter()
    karma = columns.Counter()
    up_vote_given = columns.Counter()
    up_vote_received = columns.Counter()
    down_vote_given = columns.Counter()
    down_vote_taken = columns.Counter()


class User(MBase):
    id = columns.Integer(primary_key=True)
    nick = columns.Text(required=True, index=True)

    extended = columns.Map(columns.Text, columns.Text)
    registered_at = columns.DateTime(default=dt.utcnow())
    created_at = columns.DateTime(default=dt.utcnow())


class DiscussionCounter(MBase):
    id = columns.BigInt(primary_key=True)
    message_count = columns.Counter()
    user_count = columns.Counter()
    view_count = columns.Counter()

    def to_dict(self):
        return {
            'message_count': self.message_count,
            'user_count': self.user_count,
            'view_count': self.view_count,

        }


class Discussion(MBase):
    id = columns.BigInt(primary_key=True)
    title = columns.Text(required=True)
    slug = columns.Text(required=True, index=True)
    user_id = columns.Integer()
    users = columns.Set(value_type=columns.Integer)
    post_id = columns.BigInt()
    last_message = columns.BigInt()
    published_at = columns.DateTime(default=dt.utcnow())
    topic_id = columns.Integer(required=False)

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'user_id': self.user_id,
                'post_id': self.post_id,
                'last_message': self.last_message,
                'published_at': self.published_at,
                'topic_id': self.topic_id,
        }


class DiscussionPost(MBase):
    disc_id = columns.BigInt(primary_key=True)
    post_id = columns.BigInt(primary_key=True)
    user_id = columns.Integer(primary_key=True)


class UserTimeLine(MBase):
    """
    POSTs that user will see in their timeline
    """
    user_id = columns.Integer(primary_key=True)
    post_id = columns.BigInt(primary_key=True)


class UserProject(MBase):
    """
    Projects that user follows
    """
    user_id = columns.Integer(primary_key=True)
    project_id = columns.Integer(primary_key=True)


class UserPost(MBase):
    """
    All the POSTs of a user
    """
    user_id = columns.Integer(primary_key=True)
    post_id = columns.BigInt(primary_key=True)


class UserFollower(MBase):
    """
    Followers of a user
    """
    user_id = columns.Integer(primary_key=True)
    follower_id = columns.Integer(primary_key=True)
    created_at = columns.DateTime(default=dt.utcnow())


class UserFollowing(MBase):
    """
    A user follows another user
    """
    user_id = columns.Integer(primary_key=True)
    following_id = columns.Integer(primary_key=True)
    created_at = columns.DateTime(default=dt.utcnow())


class ProjectFollower(MBase):
    project_id = columns.Integer(primary_key=True)
    user_id = columns.Integer(primary_key=True)
    created_at = columns.DateTime(default=dt.utcnow())


class PostFollower(MBase):
    post_id = columns.TimeUUID(primary_key=True)
    user_id = columns.Integer(primary_key=True)
    created_at = columns.DateTime(default=dt.utcnow())


class ChannelFollower(MBase):
    channel_id = columns.Integer(primary_key=True)
    user_id = columns.Integer(primary_key=True)
    created_at = columns.DateTime(default=dt.utcnow())


class ChannelTimeLine(MBase):
    channel_id = columns.Integer(primary_key=True)
    post_id = columns.BigInt(primary_key=True)


class ProjectTimeLine(MBase):
    project_id = columns.Integer(primary_key=True)
    post_id = columns.BigInt(primary_key=True)


class PostVote(MBase):
    post_id = columns.BigInt(primary_key=True, partition_key=True)
    user_id = columns.Integer(primary_key=True)
    positive = columns.Boolean(default=True)
    created_at = columns.DateTime(default=dt.utcnow())


class PostReply(MBase):
    post_id = columns.BigInt(primary_key=True)
    reply_post_id = columns.BigInt(primary_key=True)

