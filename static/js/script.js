function confirmDelete(event, url) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this item?')) {
        window.location.href = url;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var deleteButtons = document.querySelectorAll('.deleteButton');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var confirmDelete = confirm("你確定要刪除這個設定嗎？");
            if (!confirmDelete) {
                event.preventDefault(); // 阻止默認行為，取消刪除操作
            }
        });
    });
});