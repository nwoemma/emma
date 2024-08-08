from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Type a message...",
            }
        )
    )


class PrivateMessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Type a message...",
            }
        )
    )
