function conky_cpu_perc_padded()
    local cpu_load = tonumber(conky_parse("${cpu cpu0}")) or 0
    return string.format("%02d%%", cpu_load)
end

function conky_mem_perc_padded()
    local mem_usage = tonumber(conky_parse("${memperc}")) or 0
    return string.format("%02d%%", mem_usage)
end

function conky_fs_root_perc_padded()
    local fs_usage = tonumber(conky_parse("${fs_used_perc /}")) or 0
    return string.format("%02d%%", fs_usage)
end

function conky_fs_home_perc_padded()
    local fs_usage = tonumber(conky_parse("${fs_used_perc /home}")) or 0
    return string.format("%02d%%", fs_usage)
end

function conky_uploadspeed_formatted()    
    local speed_str = conky_parse("${upspeed enp7s0}")
    local val_mbps = 0    
    
    local num_part = string.match(speed_str, "([%d%.,]+)") 
    local unit_part = string.match(speed_str, "[%a]+$")    

    if num_part then
        
        num_part = string.gsub(num_part, ",", ".")
        local value = tonumber(num_part) or 0

        if unit_part == "MiB" or unit_part == "MB" then
            val_mbps = value * 8 -- MB/s * 8 = Mbits/s
        elseif unit_part == "KiB" or unit_part == "KB" then
            val_mbps = value * 8 / 1024 -- KB/s * 8 / 1024 = Mbits/s
        elseif unit_part == "B" then
            val_mbps = value * 8 / 1024 / 1024 -- B/s * 8 / 1024 / 1024 = Mbits/s
        end
    end

    local formatted_mbps
    if val_mbps >= 100.0 then
        formatted_mbps = string.format("%.1f", val_mbps)
    elseif val_mbps >= 10.0 then
        formatted_mbps = string.format("%5.1f", val_mbps)
    else
        formatted_mbps = string.format("%5.1f", val_mbps)
    end

    formatted_mbps = string.gsub(formatted_mbps, "%.", ",")
    return formatted_mbps
end


function conky_downloadspeed_formatted()
    local speed_str = conky_parse("${downspeed enp7s0}")
    local val_mbps = 0

    local num_part = string.match(speed_str, "([%d%.,]+)")
    local unit_part = string.match(speed_str, "[%a]+$")

    if num_part then
        num_part = string.gsub(num_part, ",", ".")
        local value = tonumber(num_part) or 0

        if unit_part == "MiB" or unit_part == "MB" then
            val_mbps = value * 8
        elseif unit_part == "KiB" or unit_part == "KB" then
            val_mbps = value * 8 / 1024
        elseif unit_part == "B" then
            val_mbps = value * 8 / 1024 / 1024
        end
    end

    local formatted_mbps
    if val_mbps >= 100.0 then
        formatted_mbps = string.format("%.1f", val_mbps)
    elseif val_mbps >= 10.0 then
        formatted_mbps = string.format("%5.1f", val_mbps)
    else
        formatted_mbps = string.format("%5.1f", val_mbps)
    end

    formatted_mbps = string.gsub(formatted_mbps, "%.", ",")
    return formatted_mbps
end