output "instance_id" { value = aws_instance.agent.id }
output "public_ip" { value = aws_instance.agent.public_ip }
output "ssm_start_session_command" {
  value = "aws ssm start-session --target ${aws_instance.agent.id} --region ${var.aws_region}"
}
output "log_group" { value = aws_cloudwatch_log_group.agent.name }
