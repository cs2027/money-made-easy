document.addEventListener('DOMContentLoaded', function() {

    // Display block for amount of remaining income (or amount over budget), assuming it is nonzero
    if (remainder != 0) {
        height_rmdr = Math.round(height * (remainder / avg));
        padding_rmdr = Math.max(min_padding, Math.round((height_rmdr - offset) / 2));

        height_str_rmdr = `${height_rmdr}` + "px";
        padding_str_rmdr = `${padding_rmdr}` + "px";

        if (height_rmdr < cutoff) {
            height_ratio = Math.round(100 * (height_rmdr / cutoff));
            document.getElementById("remainder_txt").style.fontSize = `${height_ratio}` + "%";
        }

        document.getElementById("remainder").style.height = height_str_rmdr;
        document.getElementById("remainder_txt").style.paddingTop = padding_str_rmdr;
    }

    // Block for goal savings
    height_svng = Math.round(height * (savings / avg));
    padding_svng = Math.max(min_padding, Math.round((height_svng - offset) / 2));

    height_str_svng= `${height_svng}` + "px";
    padding_str_svng = `${padding_svng}` + "px";

    if (height_svng < cutoff) {
        height_ratio = Math.round(100 * (height_svng / cutoff));
        document.getElementById("savings_txt").style.fontSize = `${height_ratio}` + "%";
    }

    document.getElementById("savings").style.height = height_str_svng;
    document.getElementById("savings_txt").style.paddingTop = padding_str_svng;

    // Blocks for each monthly expense
    for(var i = 0, length = amounts.length; i < length; i++) {
        scaled_height = Math.round(height * (amounts[i] / avg));
        padding = Math.max(min_padding, Math.round((scaled_height - offset) / 2));

        height_str = `${scaled_height}` + "px";
        padding_str = `${padding}` + "px";

        if (scaled_height < cutoff) {
            height_ratio = Math.round(100 * (scaled_height / cutoff));
            document.getElementById(`text${i}`).style.fontSize = `${height_ratio}` + "%";
        }

        document.getElementById(`expense${i}`).style.height = height_str;
        document.getElementById(`text${i}`).style.paddingTop = padding_str;
    }; 
});