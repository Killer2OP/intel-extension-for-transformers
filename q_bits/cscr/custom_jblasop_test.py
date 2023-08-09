import torch
torch.ops.load_library("build/libweight_only_jblasop.so")
activation = torch.rand(2,32, dtype=torch.float)
# raw_wei = torch.rand(256,512, dtype=torch.float)
# print(raw_wei)
# quant_wei = torch.ops.weight_only_jblasop.jblas_quantize(raw_wei,False,4,"sym",32,"fp32");
# torch.ops.weight_only_jblasop.jblas_symqdq_s4weight(raw_wei,False,32)
# print(raw_wei)
trans_raw_wei=torch.rand(3,32,dtype=torch.float)
bias=torch.rand(3,dtype=torch.float)
bias*=10
trans_quant_wei=torch.ops.weight_only_jblasop.jblas_quantize(trans_raw_wei,True,"sym",32,"fp32","s8");
# print(trans_raw_wei)
torch.ops.weight_only_jblasop.jblas_symqdq_weight(trans_raw_wei,True,"s8",32)
# trans_raw_wei=trans_raw_wei.reshape(32,2)
# print(torch.transpose(trans_raw_wei,1,0))
# correct=torch.matmul(activation,raw_wei)
trans_correct=torch.matmul(activation,torch.transpose(trans_raw_wei,1,0))
# trans_correct=torch.matmul(activation,trans_raw_wei)
trans_dst = torch.zeros(2,3,dtype=torch.float)
# dst = torch.zeros(512,512,dtype=torch.float)
# torch.ops.weight_only_jblasop.jblas_quantweight_f32_linear(activation,quant_wei,dst,512,512,256,256,512)
print("==========bias========")
print(bias)
torch.ops.weight_only_jblasop.jblas_quantweight_f32_linear_with_bias(activation,trans_quant_wei,bias,trans_dst,2,3,32,32,3,"fp32","s8")
print("==============transformat with bias result===============")
print(trans_dst)
print("~~~~~~~~~~~~~~~~~~")
print(trans_correct+bias)
torch.ops.weight_only_jblasop.jblas_quantweight_f32_linear_without_bias(activation,trans_quant_wei,trans_dst,2,3,32,32,3,"fp32","s8")
print("==============transformat without bias result===============")
print(trans_dst)
print("~~~~~~~~~~~~~~~~~~")
print(trans_correct)
# print("==============non-transformat result===============")
# print(dst)
# print("~~~~~~~~~~~~~~~~~~")
# print(correct)
