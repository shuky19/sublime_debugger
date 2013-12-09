puts RUBY_VERSION

if ["1.9.3"].include?RUBY_VERSION
  puts "SUPPORTED"
else
  puts "UNSUPPORTED"
end
