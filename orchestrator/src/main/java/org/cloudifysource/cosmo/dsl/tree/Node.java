/*******************************************************************************
 * Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

package org.cloudifysource.cosmo.dsl.tree;

import com.google.common.base.Preconditions;
import com.google.common.collect.Sets;

import java.util.Set;

/**
 * TODO: Write a short summary of this type's roles and responsibilities.
 *
 * @param <T> The node type.
 *
 * @author Dan Kilman
 * @since 0.1
 */
public class Node<T> {

    private final T value;
    private Node<T> parent;
    private final Set<Node<T>> children = Sets.newHashSet();

    Node(T value) {
        this.value = Preconditions.checkNotNull(value);
    }

    public void addChild(Node<T> child) {
        children.add(child);
    }

    public T getParentValue() {
        return parent != null ? parent.getValue() : null;
    }

    public void setParent(Node<T> parent) {
        this.parent = parent;
    }

    public T getValue() {
        return value;
    }

    public void acceptParentThenChildren(Visitor<T> visitor) {
        visitor.visit(this);
        for (Node<T> child : children) {
            child.acceptParentThenChildren(visitor);
        }
    }

}
