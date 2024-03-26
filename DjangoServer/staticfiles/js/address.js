document.addEventListener('DOMContentLoaded', function() {
    // Get the province, district, and ward select elements
    var provinceSelect = document.getElementById('id_province');
    var districtSelect = document.getElementById('id_district');
    var wardSelect = document.getElementById('id_ward');

    // When the province is changed, update the districts
    provinceSelect.addEventListener('change', function() {
        fetch('/get-districts/?province=' + provinceSelect.value)
            .then(response => response.json())
            .then(data => {
                // Clear the current districts
                while (districtSelect.firstChild) {
                    districtSelect.removeChild(districtSelect.firstChild);
                }

                // Add the new districts
                data.districts.forEach(function(district) {
                    var option = document.createElement('option');
                    option.value = district.id;
                    option.text = district.name;
                    districtSelect.appendChild(option);
                });

                // Trigger a change event to update the wards
                districtSelect.dispatchEvent(new Event('change'));
            });
    });

    // When the district is changed, update the wards
    districtSelect.addEventListener('change', function() {
        fetch('/get-wards/?district=' + districtSelect.value)
            .then(response => response.json())
            .then(data => {
                // Clear the current wards
                while (wardSelect.firstChild) {
                    wardSelect.removeChild(wardSelect.firstChild);
                }

                // Add the new wards
                data.wards.forEach(function(ward) {
                    var option = document.createElement('option');
                    option.value = ward.id;
                    option.text = ward.name;
                    wardSelect.appendChild(option);
                });
            });
    });
});