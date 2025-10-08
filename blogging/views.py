from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post, Follow
from .serializers import PostSerializer, FollowSerializer, UserSerializer
from rest_framework.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        """List current user's own posts"""
        my_posts = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def friends(self, request):
        """List posts from users you follow"""
        followed_users = request.user.following.values_list("following", flat=True)
        posts = self.queryset.filter(author_id__in=followed_users)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        target_username = request.data.get("username")
        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
        print(follow, created)
        if not created:
            return Response({"message": "Already following"}, status=status.HTTP_200_OK)

        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request):
        target_username = request.data.get("username")
        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = Follow.objects.filter(follower=request.user, following=target_user).delete()
        if deleted:
            return Response({"message": f"Unfollowed {target_username}"}, status=status.HTTP_200_OK)
        return Response({"message": "You were not following this user"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def followers(self, request):
        followers = Follow.objects.filter(following=request.user)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def following(self, request):
        following = Follow.objects.filter(follower=request.user)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
