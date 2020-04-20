function VkUsed() {
  var checkBox = document.getElementById("checkboxVkUsed");
  var elem = document.getElementById("vk_id");

  if (checkBox.checked == true){
    elem.style.display = "block";
  } else {
    elem.style.display = "none";
  }
}
