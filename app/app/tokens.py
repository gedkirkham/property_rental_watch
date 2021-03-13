from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ReviewActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )


review_activation_token = ReviewActivationTokenGenerator()
