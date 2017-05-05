var Landing = (function() {
	
	return {
		init: function() {
			$('#id_country').on('change', function(e){
				var country = $($(this).children()[$(this).prop('selectedIndex')]).attr('value'),
					url = '/number/get_cc/' + country + '/';
				$('#number-form').find('small.red-text').remove();
				$.ajax({
					url: url,
					type: 'GET',
					data: {},
					success: function(data, status, xhr){
						code = data['calling_code'];
						$calling_code = $('#id_calling_code');
						$calling_code.prop('disabled', false);
						if (!code){
							$('#number-form').prepend($('<small class="red-text">Could not find calling code for this country in our DB. Please enter the correct calling code for this country.</small>'))
							$calling_code.attr('value', '');
							document.getElementById('id_calling_code').value = '';
						}
						else {
							$calling_code.attr('value', code);
							document.getElementById('id_calling_code').value = code;
						}
					},
				});
			});
		}
	}
})();
