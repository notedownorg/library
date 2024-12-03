// Copyright 2024 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package plugin

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os/exec"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type PluginConfig struct {
	// The version of the plugin protocol in use
	ProtocolVersion int `json:"protocol_version,omitempty"`

	// The grpc address the plugin is listening on
	Address string `json:"address"`

	// The version of the plugin itself
	// This isnt currently used but could be useful in the future
	Version string `json:"version,omitempty"`
}

type pluginConn struct {
	*grpc.ClientConn
}

func NewConnection(command string) (*pluginConn, error) {
	cmd := exec.Command("sh", "-c", command)

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return nil, fmt.Errorf("failed to get stdout pipe: %w", err)
	}

	if err := cmd.Start(); err != nil {
		return nil, fmt.Errorf("failed to run plugin command: %w", err)
	}

	scanner := bufio.NewScanner(stdout)
	if !scanner.Scan() {
		if err := scanner.Err(); err != nil {
			return nil, fmt.Errorf("failed to read plugin output: %w", err)
		}
		return nil, fmt.Errorf("plugin output is empty")
	}

	line := scanner.Bytes()

	// We can now use the line to setup the plugin
	var plugin PluginConfig
	if err := json.Unmarshal(line, &plugin); err != nil {
		return nil, fmt.Errorf("failed to unmarshal plugin: %w", err)
	}

	conn, err := grpc.NewClient(plugin.Address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, fmt.Errorf("failed to dial grpc: %w", err)
	}

	return &pluginConn{ClientConn: conn}, nil
}

func (c *pluginConn) Close() {
	c.ClientConn.Close()
}
