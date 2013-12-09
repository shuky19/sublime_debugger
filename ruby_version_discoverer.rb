puts RUBY_VERSION

if ["1.9.3", "2.0.0"].include?RUBY_VERSION
  puts "SUPPORTED"
else
  puts "UNSUPPORTED"
end
